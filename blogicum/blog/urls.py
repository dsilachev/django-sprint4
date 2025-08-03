from django.urls import include, path
from . import views

app_name = 'blog'

urlpatterns = [
    # Главная страница
    path('', views.PostListView.as_view(), name='index'),

    # Посты
    path('posts/', include([
        path('create/',
            views.PostCreateView.as_view(),
            name='create_post'),

        path('<int:post_id>/', include([
            path('',
                views.PostDetailView.as_view(),
                name='post_detail'),
            path('edit/',
                views.PostUpdateView.as_view(),
                name='edit_post'),
            path('delete/',
                views.PostDeleteView.as_view(),
                name='delete_post'),

            path('comment/',
                views.CommentCreateView.as_view(),
                name='add_comment'),

            path('edit_comment/<int:comment_id>/',
                views.CommentUpdateView.as_view(),
                name='edit_comment'),

            path('delete_comment/<int:comment_id>/',
                views.CommentDeleteView.as_view(),
                name='delete_comment'),
        ])),
    ])),

    # Профили
    path('profile/', include([
        path('<str:username>/',
            views.ProfileListView.as_view(),
            name='profile'),
        path('',
            views.ProfileUpdateView.as_view(),
            name='edit_profile'),
    ])),

    # Категории
    path('category/<slug:category_slug>/',
        views.CategoryListView.as_view(),
        name='category_posts'),
]
