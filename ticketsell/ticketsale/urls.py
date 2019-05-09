from django.conf.urls import url, include
from . import views
from  rest_framework.routers import DefaultRouter
from django.views import static
from django.conf import settings

# 创建路由器并注册我们的视图
router = DefaultRouter()
router.register(r'tickets', views.TicketsViewSet, base_name='tickets')

app_name = 'ticketsale'

urlpatterns = [
        url(r'', views.index_start, name='home'),
        url(r'register_after/', views.register, name='register_after'),
        url(r'login_after/', views.login, name='login_after'),
        url(r'tickets_search/', views.tickets_search, name="tickets_search"),
        url(r'user_home/', views.index_end, name='user_home'),


        url(r'^static/(?P<path>.*)$', static.serve, {'document_root':settings.STATIC_URL}, name='static'),
        # API路由
        url(r'^api/', include(router.urls))
]