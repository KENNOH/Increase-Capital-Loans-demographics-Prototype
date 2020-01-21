"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^upload/', views.upload, name='upload'),
    url(r'^display/', views.display, name='display'),
    url(r'^customers/', views.customers, name='customers'),
    url(r'^repayments/', views.repayments, name='repayments'),
    url(r'^filter/', views.process_filter, name='process_filter'),
    url(r'^search/', views.search, name='search'),
    url(r'^expand_customer/(?P<customer_id>[0-9]+)/',views.expand_customer, name='expand_customer'),
]
