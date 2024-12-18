from django.urls import path
from . import views


urlpatterns = [
    # 게시글 작성
    path('article_create/', views.article_create),
    path('article/<int:article_pk>/detail_update_delete/', views.article_detail_update_delete),
    
    # 댓글 작성
    path('article/<int:article_pk>/comment_create/', views.comment_create),
    path('article/<int:article_pk>/comment/<int:comment_pk>/detail_update_delete/', views.comment_detail_update_delete),
    # path('article/<int:article_pk>/comment/<int:comment_pk>/reply/', views.comment_reply),
    path('article/<int:article_pk>/comment/<int:comment_id>/like/', views.like_comment),

    # 달성 체크 url
    path('article/<int:article_pk>/is_completed/', views.is_complete),
    #각 카테고리 메인 페이지
    path('<str:category_name>/', views.category_main),
    # 전체 메인 페이지
    path('', views.main),
]