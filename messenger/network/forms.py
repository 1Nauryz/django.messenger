from django import forms
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField


from .models import *


class AddPostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Category not selected"

    class Meta:
        model = Message
        fields = ['slug', 'fromWhom', 'toWhom', 'content', 'photo', 'is_published', 'cat']
        widgets = {
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 8}),
        }
        captcha = CaptchaField()

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) < 20:
            raise ValidationError('Minimum content length 20 characters')
        return content