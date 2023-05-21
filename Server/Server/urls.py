"""
URL configuration for Server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

import MyApp.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', MyApp.views.user),
    path('follow/', MyApp.views.follow),
    path('block/', MyApp.views.block),
    path('message/', MyApp.views.message),
    path('session/', MyApp.views.session),
    path('post/', MyApp.views.post),
    path('likes/', MyApp.views.likes),
    path('favorites/', MyApp.views.favorites),
    path('comments/', MyApp.views.comments),
    path('notification/', MyApp.views.notification),
]
