"""ticketsell URL Configuration

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
from django.urls import path
from django.conf.urls import url, include
from django.views import static
from ticketsale import views
from django.conf import settings
from rest_framework.routers import DefaultRouter
# 创建路由器并注册我们的视图。
router = DefaultRouter()
router.register(r'tickets', views.TicketsViewSet, base_name="tickets")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_start, name='home'),
    path('user_home/', views.index_end, name="user_home"),
    path('tickets_search/', views.tickets_search, name="tickets_search"),
    path('ticket_buy/', views.ticket_buy, name="ticket_buy"),
    path('register_after/', views.register, name="register_after"),
    path('login_after/', views.login, name="login_after"),
    path('order_search/', views.order_search, name="order_search"),
    path('order_cancel', views.order_cancel, name="order_cancel"),
    url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_URL}, name='static'),
    # API路由
    url(r'^api/', include(router.urls))
]

