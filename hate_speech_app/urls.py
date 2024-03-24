from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('chart/', views.chart, name='chart'),
    path('performance/', views.performance, name='performance'),
    path('toxic/', views.toxic, name='toxic'),
    path('predict/', views.predict, name='predict'),
    path('logout/', views.logout_view, name='logout'),

]
