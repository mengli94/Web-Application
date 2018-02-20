"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth import views
import grumblr.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', grumblr.views.home, name = 'home'),
    url(r'^grumblr/*$', grumblr.views.home),
    url(r'^grumblr/profile/(?P<username>\w+)$', grumblr.views.profile),
    url(r'^grumblr/login$', views.login, {'template_name':'grumblr/login.html'}, name='login'),
    url(r'^grumblr/logout$', views.logout_then_login, name='logout'),
    url(r'^grumblr/register$', grumblr.views.register, name='register'),
    url(r'^grumblr/add_post$', grumblr.views.add_post, name='add_post'),
]
