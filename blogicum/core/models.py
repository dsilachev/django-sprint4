from django.db import models
from blog.constants import COUNT_CHAR_DISPLAYED


class PublishedModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Уберите галочку, чтобы скрыть публикацию.',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )

    class Meta:
        abstract = True


class TitleModel(PublishedModel):

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок',
        help_text='Название, не более 256 символов.',
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title[:COUNT_CHAR_DISPLAYED]
