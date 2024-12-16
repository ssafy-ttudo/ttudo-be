# settings.py 에서 설정한 MAIN_DOMAIN 등을 불러오기 위해 import 함
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_list_or_404, get_object_or_404
import requests
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .models import User, UserList


# main domain(http://127.0.0.1:8000)
main_domain = settings.MAIN_DOMAIN

## NAVER

# DRF의 APIView를 상속받아 View를 구성
class NaverLoginAPIView(APIView):
    # 로그인을 위한 창은 누구든 접속이 가능해야 하기 때문에 permission을 AllowAny로 설정
    permission_classes = (AllowAny,)
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('mypage:mypage')
        
        client_id = settings.NAVER_CLIENT_ID
        response_type = "code"
        # Naver에서 설정했던 callback url을 입력해주어야 한다.
        # 아래의 전체 값은 http://127.0.0.1:8000/user/naver/callback 이 된다.
        uri = main_domain + "/accounts/naver/callback/"
        state = settings.NAVER_STATE
        # Naver Document 에서 확인했던 요청 url
        url = "https://nid.naver.com/oauth2.0/authorize"
        
        # Document에 나와있는 요소들을 담아서 요청한다.
        return redirect(
            f'{url}?response_type={response_type}&client_id={client_id}&redirect_uri={uri}&state={state}'
        )
        
        
class NaverCallbackAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        try:
            # 네이버에서 보낸 인증 코드와 상태값을 받음
            code = request.GET.get("code")
            state = request.GET.get("state")

            if not code or not state:
                return Response({"error": "Missing code or state"}, status=400)

            # 토큰 요청 URL 및 파라미터 설정
            token_url = "https://nid.naver.com/oauth2.0/token"
            params = {
                "grant_type": "authorization_code",
                "client_id": settings.NAVER_CLIENT_ID,
                "client_secret": settings.NAVER_CLIENT_SECRET,
                "code": code,
                "state": state,
            }

            # 네이버 서버에 토큰 요청
            response = requests.post(token_url, params=params)
            token_data = response.json()

            if "access_token" not in token_data:
                return Response({"error": "Token request failed"}, status=400)

            # 사용자 정보 요청
            access_token = token_data["access_token"]
            user_info_url = "https://openapi.naver.com/v1/nid/me"
            headers = {"Authorization": f"Bearer {access_token}"}
            user_info_response = requests.get(user_info_url, headers=headers)
            user_info = user_info_response.json()
            
            # 사용자 정보 저장
            
            nickname = user_info['response']['name']
            social_id = user_info['response']['id']
            profile_img = user_info['response']['profile_image']
            
            user = User(username=social_id, nickname=nickname, social_id=social_id, profile_img=profile_img)
            

                
            # 사용자 조회와 로그인
            user, created = User.objects.get_or_create(
                social_id=social_id,
                defaults={
                    'nickname' : nickname,
                    'profile_img': profile_img,
                    'username':social_id,
                    'social':'NAVER',
                }
            )
            
            user.access_token = token_data.get("access_token")
            user.refresh_token = token_data.get("refresh_token")
            user.save()

            # 혹시 토큰 안 받아와지면 django에서 제공하는 토큰 생성
            # token, _ = Token.objects.get_or_create(user=user)
            
            login(request, user)
            
            
            
            # 사용자 정보 반환 (예: 프론트엔드로 전달)
            return redirect('mypage:mypage')
            # return Response({'token_key':token.key, 'token':token}, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            print(f"에러 발생: {e}")
            return Response({"error": "Internal Server Error"}, status=500)
        

## KAKAO

# DRF의 APIView를 상속받아 View를 구성
class KakaoLoginAPIView(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('mypage:mypage')
        
        client_id = settings.KAKAO_CLIENT_ID
        response_type = "code"
        uri = main_domain + "accounts/kakao/callback/"
        # 필수 아님
        # state = settings.KAKAO_STATE
        # Kakao Document 에서 확인했던 요청 url
        url = "https://kauth.kakao.com/oauth/authorize"
        
        # Document에 나와있는 요소들을 담아서 요청한다.
        return redirect(
            f'{url}?response_type={response_type}&client_id={client_id}&redirect_uri={uri}'
        )
        
class KakaoCallbackAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        print(code)
        
        if not code:
            error = request.GET.get('error')
            error_description = request.GET.get('error_description')
            return Response({error: error_description}, status=status.HTTP_400_BAD_REQUEST)
        
        grant_type = 'authorization_code'
        client_id = settings.KAKAO_CLIENT_ID
        client_secret = settings.KAKAO_CLIENT_SECRET
        redirect_uri = 'http://127.0.0.1:8000/accounts/kakao/callback/'

        
        token_req = requests.post(
            "https://kauth.kakao.com/oauth/token",
            headers={
                "Content-type": "application/x-www-form-urlencoded"
            },
            data={
                "grant_type":grant_type,
                "client_id":client_id,
                "redirect_uri":redirect_uri,
                "code":code,
                "client_secret":client_secret,
            }
        )
        
        token_req_json = token_req.json()
        # print(token_req_json)
        access_token = token_req_json.get('access_token')
        print("Token request response:", token_req.text)

        
        if not access_token:
            return Response({'error':'Failed to obtain access token.'}, status=status.HTTP_400_BAD_REQUEST)
        
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={
                "Authorization" : f"Bearer {access_token}"
            },
        )
        profile_json = profile_request.json()
        kakao_account = profile_json.get('kakao_account')
        social_id = profile_json.get('id')
        
        if not kakao_account:
            return Response({'error':'Failed to obtain user info.'}, status=status.HTTP_400_BAD_REQUEST)
        
        profile = kakao_account.get('profile')
        nickname = profile.get('nickname')
        profile_img = profile.get('profile_image_url')
        # print('================================')
        # print(nickname)
        # print(profile_img)
        # print(social_id)
        
        user, created = User.objects.get_or_create(
            social_id=social_id,
            defaults={
                'nickname': nickname,
                'profile_img': profile_img,
                'username': social_id,
                'social': 'KAKAO',
                'access_token': token_req_json.get('access_token'),
                'refresh_token': token_req_json.get('refresh_token'),
            }
        )

        if not created:
            user.access_token = token_req_json.get('access_token')
            user.refresh_token = token_req_json.get('refresh_token')
            user.save()

        # 혹시 토큰 안 받아와지면 django에서 제공하는 토큰 생성
        # token, _ = Token.objects.get_or_create(user=user)
        
        login(request, user)
        login(request, user)
        return Response({
            'message': '로그인 성공',
            'access_token': token_req_json.get('access_token'),
            'refresh_token': token_req_json.get('refresh_token'),
            'user_id': user.id
        }, status=status.HTTP_200_OK)

        # return Response(status=status.HTTP_202_ACCEPTED)
    
### 로그아웃
@login_required
def logout(request):
    auth_logout(request)
    print(request.user)
    return redirect('accounts:index')
    
from .serializers import UserInfoSerializer, UserListSerializer


### 마이페이지
# @api_view(['GET'])
# def mypage(request):
#     if request.method == 'GET':
#         if request.user.is_authenticated:
#             current_user = request.user
#             # print(current_user)
#             # print('-------------------')
#             user_queryset = User.objects.filter(social_id=current_user)
#             # print(user_queryset)
#             serializer = UserInfoSerializer(user_queryset, many=True)
#             # print(serializer.data)
            
#             return Response(serializer.data, status=status.HTTP_200_OK)
#     return Response(status=status.HTTP_401_UNAUTHORIZED)

# ### 친구 추가
# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def friend(request):
#     # 나 (팔로우 하는 사람)
#     me = User.objects.filter(social_id=request.user)
#     # print(request.data.get('friend_id'))
#     if request.method == 'GET':
#         users = User.objects.all().exclude(social_id=request.user)
#         serializer = UserListSerializer(users, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         friend_id = request.data.get('friend_id')
#         if not friend:
#             return Response({'error': 'Friend_id is required.'}, status=status.HTTP_400_BAD_REQUEST)
#         try:
#             friend = User.objects.get(id=friend_id)
#         except User.DoesNotExist:
#             return Response({'error':'User not found.'}, status=status.HTTP_404_NOT_FOUND)
#         friendship, created = UserList.objects.get_or_create(
#             user=me, friend=friend
#         )
#         # 내 즐겨찾기에 상대방이 없다면
#         # 팔로우
#         if created:
#             return Response({'message':'Friend added successfully.'}, status=status.HTTP_201_CREATED)
#         # 내 즐겨찾기에 상대방이 있다면
#         # 언팔로우
#         else:
#             friendship.delete()
#             return Response({'message':'Friend removed successfully.'}, status=status.HTTP_200_OK)     
        
#     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)