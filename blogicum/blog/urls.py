from django.urls import include, path
from . import views

app_name = 'blog'

urlpatterns = [
    # Мэйн
    path('', views.PostListView.as_view(), name='index'),

    # Посты
    path('posts/', include([
        # Создание нового поста
        path('create/', views.PostCreateView.as_view(), name='create_post'),

        path('<int:post_id>/', include([
            # Просмотр поста
            path('', views.PostDetailView.as_view(), name='post_detail'),

            # Редактирование поста
            path('edit/', views.PostUpdateView.as_view(), name='edit_post'),

            # Удаление поста
            path('delete/', views.PostDeleteView.as_view(), name='delete_post'),

            # Комменты к посту
            path('comment/', views.CommentCreateView.as_view(), name='add_comment'),

            # Редактирование коммента
            path(
                'edit_comment/<int:comment_id>/',
                views.CommentUpdateView.as_view(),
                name='edit_comment'
            ),

            # Удаление коммента
            path(
                'delete_comment/<int:comment_id>/',
                views.CommentDeleteView.as_view(),
                name='delete_comment'
            ),
        ])),
    ])),

    # Профили пользователей
    path('profile/', include([
        # Просмотр чужого профиля
        path('<str:username>/', views.ProfileListView.as_view(), name='profile'),

        # Редактирование своего профиля
        path('', views.ProfileUpdateView.as_view(), name='edit_profile'),
    ])),

    # Посты по категориям
    path(
        'category/<slug:category_slug>/',
        views.CategoryListView.as_view(),
        name='category_posts'
    ),
]