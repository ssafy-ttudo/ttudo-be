from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    ### 로그인
    # 여기서 callback url은 반드시 Naver 로그인 API 설정 당시 작성했던
    # callback url로 지정해주어야 한다. 앞의 user/ 까지 더해지면
    # http://127.0.0.1:8000/user/naver/callback 이 된다.
    
    ## NAVER
    path('naver/login/', views.NaverLoginAPIView.as_view(), name='naver_login'),
    path('naver/callback/', views.NaverCallbackAPIView.as_view(), name='naver_callback'),
    
    ## KAKAO
    path('kakao/login/', views.KakaoLoginAPIView.as_view(), name='kakao_login'),
    path('kakao/callback/', views.KakaoCallbackAPIView.as_view(), name='kakao_callback'),
    
    ### 로그아웃
    path('logout/', views.logout, name='logout'),
    
    ### 마이페이지
    # path('mypage/', views.mypage, name='mypage'),
    
    ### 친구 추가
    path('friend/', views.friend, name='friend'),
]
