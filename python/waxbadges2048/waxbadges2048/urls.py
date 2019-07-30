"""waxbadges2048 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('__admin/', admin.site.urls),

    path('accounts/', include('allauth.urls')),

    path('robots.txt', TemplateView.as_view(template_name='misc/robots.txt', content_type='text/plain')),
    path('privacy_policy.html', TemplateView.as_view(template_name='misc/privacy_policy.html')),

    path('ajax/get_granted_achievements', views.GetGrantedAchievementsAjaxView.as_view()),
    path('ajax/grant_achievement', views.GrantAchievementAjaxView.as_view()),
    path('', views.IndexView.as_view()),
]
