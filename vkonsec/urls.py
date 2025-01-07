"""
URL configuration for vkonsec project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from database import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index, name='home'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/',views.dashboardindex, name='dashboard'),
    path('login/',views.dashboardlogin, name='login'),
    path('dologout/', views.logout_user, name='doLogout'),

    #course page
    path('network/', views.network, name='network'),
    path('devops/', views.devops,name='devops'),
    path('ceh/',views.ceh,name="ceh"),
    path('checkpoint/',views.checkpoint,name='checkpoint'),
    path('pcnsa/',views.PCNSA,name='pcnsa'),
    path('soc/',views.soccourse,name='soc'),
    path('ccna/',views.CCNA,name='soc'),
    path('mars/',views.mars,name='mars')
]
