pipeline {
    agent {
        label 'agent47'
    }
    tools {
        maven 'maven3'
        jdk 'jdk17'
    }
    stages{
        stage("Fetch the code"){
            steps{
                git url: 'https://github.com/hkhcoder/vprofile-project.git', branch: 'atom'
            }
        }
        stage('Build'){
            steps{
                sh 'mvn clean install -DskipTests'
            }
        }
        stage('Test'){
            steps{
                sh 'mvn test'
            }
        }
        stage('Code analysis with checkstyle'){
          
		  environment {
             scannerHome = tool 'sonarserver'
          }

          steps {
            withSonarQubeEnv('sonarserver') {
               sh '''${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=vprofile \
                   -Dsonar.projectName=vprofile-repo \
                   -Dsonar.projectVersion=1.0 \
                   -Dsonar.sources=src/ \
                   -Dsonar.java.binaries=target/test-classes/com/visualpathit/account/controllerTest/ \
                   -Dsonar.junit.reportsPath=target/surefire-reports/ \
                   -Dsonar.jacoco.reportsPath=target/jacoco.exec \
                   -Dsonar.java.checkstyle.reportPaths=target/checkstyle-result.xml'''
            }
        }
    }
    stage('upload artifact'){
        steps {
            nexusArtifactUploader(
                nexusVersion: 'nexus3',
                protocol: 'http',
                nexusUrl: '172.31.18.61:8081',
                groupId: 'QA',
                version: '${env.BUILD_ID}.${env.BUILD_TIMESTAMP}',
                repository: 'projectrepo',
                credentialsId: 'nexuscred',
                artifacts: [
                    [artifactId: 'vproapp',
                    classifier: '',
                    file: 'target/vprofile-v2.war',
                    type: 'war']
        ]
     )

        }
    }
        
    }
    
    post {
        success {
            slackSend(channel: '#all-javacicdproject', color: 'good', message: "Build #${env.BUILD_NUMBER} succeeded!")
        }
        failure {
            slackSend(channel: '#all-javacicdproject', color: 'danger', message: "Build #${env.BUILD_NUMBER} failed.")
        }
        always {
            slackSend(channel: '#all-javacicdproject', color: 'warning', message: "Build #${env.BUILD_NUMBER} completed.")
        }
    }
}