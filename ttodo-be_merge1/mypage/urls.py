from django.urls import path
from . import views

app_name = 'mypage'

urlpatterns = [
    path('', views.user_profile_view, name='mypage'),
    path('<str:username>/', views.user_profile_view, name='user_profile'),
    path('users/', views.user_list, name='user_list'),
    path('follow/', views.follow_unfollow, name='follow_unfollow'),
]
