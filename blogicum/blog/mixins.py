from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Count
from django.urls import reverse
from django.utils import timezone

from blog.models import Comment, Post


class PostQueryMixin:
    """Работа со статьями."""

    def get_posts(self):
        return (
            Post.objects
            .select_related('category', 'author', 'location')
            .annotate(comment_count=Count('comments'))
            .order_by('-pub_date')
        )

    def get_posts_with_filter(self):
        return (
            self.get_posts()
            .filter(
                is_published=True,
                category__is_published=True,
                pub_date__lte=timezone.now()
            )
        )


class PostMixin:
    """Настройки для формы постов."""

    model = Post
    template_name = 'blog/create.html'


class AuthorMixin(UserPassesTestMixin):
    """Проверяет, является ли пользователь автором."""

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class CommentMixin:
    """Настройки для формы комментариев."""

    model = Comment
    template_name = 'blog/comment.html'


class ProfileUrlMixin:
    """Перенаправляет в профиль после действий."""

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostDetailMixin:
    """Перенаправляет на страницу поста."""

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )
