from django.urls import path
from . import views

urlpatterns = [
    path('', views.mypage_view, name='mypage'),
    path('users/', views.user_list, name='user_list'),
    path('follow/', views.follow_unfollow, name='follow_unfollow'),
]
