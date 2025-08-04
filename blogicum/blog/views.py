from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from blogicum.constants import COUNT_POST_DISPLAYED
from blog.forms import CommentForm, PostForm
from blog.models import Category, Post
from blog.mixins import (
    AuthorMixin, CommentMixin, PostDetailMixin, PostMixin,
    PostQueryMixin, ProfileUrlMixin
)


class PostListView(ListView, PostQueryMixin):
    template_name = 'blog/index.html'
    paginate_by = COUNT_POST_DISPLAYED

    def get_queryset(self):
        return self.get_posts_with_filter()


class CategoryListView(ListView, PostQueryMixin):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = COUNT_POST_DISPLAYED

    def get_category(self):
        return get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )

    def get_queryset(self):
        return self.get_posts_with_filter().filter(
            category=self.get_category()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context


class PostCreateView(
    LoginRequiredMixin, PostMixin, ProfileUrlMixin, CreateView
):
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(
    LoginRequiredMixin, AuthorMixin, PostMixin, PostDetailMixin, UpdateView
):
    form_class = PostForm
    pk_url_kwarg = 'post_id'

    def handle_no_permission(self):
        return redirect(
            reverse(
                'blog:post_detail',
                kwargs={'post_id': self.kwargs.get('post_id')}
            )
        )


class PostDeleteView(
    LoginRequiredMixin, AuthorMixin, PostMixin, ProfileUrlMixin, DeleteView
):
    pk_url_kwarg = 'post_id'


class PostDetailView(DetailView, PostQueryMixin, PostDetailMixin):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        if self.request.user != post.author:
            return get_object_or_404(
                self.get_posts_with_filter(),
                pk=self.kwargs['post_id']
            )
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form': CommentForm(),
            'comments': self.object.comments.select_related('author')
        })
        return context


class ProfileListView(ListView, PostQueryMixin):
    template_name = 'blog/profile.html'
    paginate_by = COUNT_POST_DISPLAYED

    def get_user(self):
        return get_object_or_404(
            User,
            username=self.kwargs['username']
        )

    def get_queryset(self):
        if self.request.user == self.get_user():
            return self.get_posts().filter(author=self.get_user())
        return self.get_posts_with_filter().filter(author=self.get_user())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_user()
        return context


class ProfileUpdateView(LoginRequiredMixin, ProfileUrlMixin, UpdateView):
    model = User
    fields = ('username', 'first_name', 'last_name', 'email')
    template_name = 'blog/profile_edit.html'

    def get_object(self, queryset=None):
        return self.request.user


class CommentCreateView(LoginRequiredMixin, CommentMixin, CreateView):
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post = get_object_or_404(
            Post,
            pk=self.kwargs['post_id']
        )
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class CommentUpdateView(
    LoginRequiredMixin, AuthorMixin, CommentMixin, PostDetailMixin, UpdateView
):
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'


class CommentDeleteView(
    LoginRequiredMixin, AuthorMixin, CommentMixin, PostDetailMixin, DeleteView
):
    pk_url_kwarg = 'comment_id'
