def COLOR_MAP = [
    'success': 'good',
    'FAILURE': 'danger',
]
pipeline {
    agent any

    parameters {
        choice(name: 'DEPLOY_ENV', choices: ['blue', 'green'], description: 'Choose which environment to deploy: Blue or Green')
        booleanParam(name: 'SWITCH_TRAFFIC', defaultValue: false, description: 'Switch traffic between Blue and Green')
    }

    stages{
        stage('clean workspace'){
            steps{
                cleanWs()
            }
        }

        stage('Fetch the code'){
            steps{
                git url: 'https://github.com/bhaktraj/vkonsec.git', branch: 'docker'

            }    
        }
        
        stage('TRIVY FS SCAN') {
            steps {
                sh "trivy fs . > trivyfs.txt"
            }
        }
        
        stage('sonarqube scan'){
            environment {
             scannerHome = tool 'Sonarscanner'
          }

          steps {
            withSonarQubeEnv('Sonarscanner') {
               sh '''${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=vkonsec \
                   -Dsonar.projectName=vkonsec \
                   -Dsonar.projectVersion=1.0 \
                   -Dsonar.sources=. \
                   '''
            }
        }
        }
        stage('OWASP Dependency Check') {
            steps {
                dependencyCheck additionalArguments: '--scan ./ --format XML --out dependency-check-report --project vkonsec-django --enableExperimental', odcInstallation: 'Owasp'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
                
            }
        }
        stage('Build docker images'){
            steps{
                script{
                    dockerimage = docker.build('vkonsec' + ":$BUILD_NUMBER", ".")
                    dockerimage = docker.build('nginx' + ":$BUILD_NUMBER", "./nginx")

                }

            }
        }
        stage("TRIVY"){
            steps{
                sh "trivy image vkonsec:$BUILD_NUMBER > trivy.txt" 
            }
        }
        stage("Docker Push"){
            steps{
                script{
                   withDockerRegistry(credentialsId: 'dockercred', toolName: 'docker'){   
                       sh "docker tag vkonsec:$BUILD_NUMBER bhaktraj/vkonsec:$BUILD_NUMBER "
                       sh "docker tag nginx:$BUILD_NUMBER bhaktraj/nginx:$BUILD_NUMBER "
                       sh "docker push bhaktraj/vkonsec:$BUILD_NUMBER "
                       sh "docker push bhaktraj/nginx:$BUILD_NUMBER "
                    }
                }
            }
        }
        stage('Persistent Volume Claim for MySQL') {
            steps {
                script {
                    withKubeConfig(caCertificate: '', clusterName: 'blue-green-deployment', contextName: '', credentialsId: 'k8-token', namespace: 'webapps', restrictKubeConfigAccess: false, serverUrl: 'https://46743932FDE6B34C74566F392E30CABA.gr7.ap-south-1.eks.amazonaws.com') {
                        sh """ if ! kubectl get pvc mysql-pvc -n webapps; then
                                kubectl apply -f k8/mysql-pvc.yaml -n webapps
                            fi
                        """  
                    }
                }
            }
        }
        stage('Deploying MySQL') {
            steps {
                script {
                    withKubeConfig(caCertificate: '', clusterName: 'blue-green-deployment', contextName: '', credentialsId: 'k8-token', namespace: 'webapps', restrictKubeConfigAccess: false, serverUrl: 'https://46743932FDE6B34C74566F392E30CABA.gr7.ap-south-1.eks.amazonaws.com') {
                        sh """ 
                        kubectl apply -f k8/mysql-deployment.yaml -n webapps
                        kubectl apply -f k8/mysql-service.yaml -n webapps
                        """  
                    }
                }
            }
        }

        stage('Update K8s Manifest') {
            steps {
                sh " sed 's/buildid/$BUILD_NUMBER/g' k8/django-blue-deployment.yaml "
                sh " sed 's/buildid/$BUILD_NUMBER/g' k8/django-green-deployment.yaml "
                sh " sed 's/buildid/$BUILD_NUMBER/g' k8/nginx-deployment.yaml "
            }
        }

        stage('Application deployment') {
            steps {
                script {
                    def deploymentFile = ""
                    if (params.DEPLOY_ENV == 'blue') {
                        deploymentFile = 'django-blue-deployment.yaml'
                    } else {
                        deploymentFile = 'django-green-deployment.yaml'
                    }

                    withKubeConfig(caCertificate: '', clusterName: 'blue-green-deployment', contextName: '', credentialsId: 'k8-token', namespace: 'webapps', restrictKubeConfigAccess: false, serverUrl: 'https://46743932FDE6B34C74566F392E30CABA.gr7.ap-south-1.eks.amazonaws.com') 
                    {
                        sh "kubectl apply -f ${deploymentFile} -n webapps"
                    }
                }
            }
        }

        stage('Deploy Nginx') {
            steps {
                script {
                    withKubeConfig(caCertificate: '', clusterName: 'blue-green-deployment', contextName: '', credentialsId: 'k8-token', namespace: 'webapps', restrictKubeConfigAccess: false, serverUrl: 'https://46743932FDE6B34C74566F392E30CABA.gr7.ap-south-1.eks.amazonaws.com') {
                        sh """ 
                        kubectl apply -f k8/nginx-deployment.yaml -n webapps
                        kubectl apply -f k8/nginx-service.yaml -n webapps
                        """  
                    }
                }
            }
        }

        stage('Switch Traffic Between Blue & Green Environment') {
            when {
                expression { return params.SWITCH_TRAFFIC }
            }
            steps {
                script {
                    def newEnv = params.DEPLOY_ENV

                    // Always switch traffic based on DEPLOY_ENV
                    withKubeConfig(caCertificate: '', clusterName: 'blue-green-deployment', contextName: '', credentialsId: 'k8-token', namespace: 'webapps', restrictKubeConfigAccess: false, serverUrl: 'https://46743932FDE6B34C74566F392E30CABA.gr7.ap-south-1.eks.amazonaws.com') {
                        sh '''
                            kubectl patch service djangoapp -p "{\\"spec\\": {\\"selector\\": {\\"app\\": \\"bankapp\\", \\"version\\": \\"''' + newEnv + '''\\"}}}" -n webapps
                        '''
                    }
                    echo "Traffic has been switched to the ${newEnv} environment."
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                script {
                    def verifyEnv = params.DEPLOY_ENV
                    withKubeConfig(caCertificate: '', clusterName: 'blue-green-deployment', contextName: '', credentialsId: 'k8-token', namespace: 'webapps', restrictKubeConfigAccess: false, serverUrl: 'https://46743932FDE6B34C74566F392E30CABA.gr7.ap-south-1.eks.amazonaws.com') {
                        sh """
                        kubectl get pods -l version=${verifyEnv} -n webapps
                        kubectl get svc djangoapp -n webapps
                        """
                    }
                }
            }
        }
        

        
    }
    post {
        always {
            echo 'slack Notification'
            slackSend channel: '#jenkins',
                color:  COLOR_MAP[currentBuild.currentResult],
                message:"*${currentBuild.currentResult}:* Job ${env.JOB_NAME} build ${env.BUILD_NUMBER} \n more info at : ${env.BUILD_URL}"
        }
    }
}