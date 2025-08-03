from django import forms
from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)
        localized_fields = ('pub_date',)
        widgets = {
            'text': forms.Textarea(attrs={
                'cols': '22',
                'rows': '5',
                'class': 'form-text'
            }),
            'pub_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'step': '300',
                    'class': 'form-datetime'
                },
                format='%Y-%m-%dT%H:%M'
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': '3',
                'placeholder': 'Ваш комментарий...'
            })
        }
