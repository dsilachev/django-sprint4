from django.contrib import admin
from .models import Post, Category, Location, Comment

admin.site.empty_value_display = 'Не задано'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'is_published',
        'created_at',
        'category',
        'author',
        'location',
    )
    list_editable = (
        'is_published',
        'text',
        'category',
        'author',
        'location',
    )
    search_fields = ('title',)
    list_filter = (
        'category',
        'author',
        'location',
        'is_published',
    )
    list_display_links = ('title',)


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (PostInline,)
    list_display = ('title',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    inlines = (PostInline,)
    list_display = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text', 'author', 'post'
    )
    list_filter = (
        'author', 'post'
    )
    search_fields = ('text',)