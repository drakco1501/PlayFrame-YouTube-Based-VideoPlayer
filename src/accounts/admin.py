from django.contrib import admin
from .models import *

from django import forms
from django.core.exceptions import ValidationError
import mimetypes

class VideoAdminForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = '__all__'
        widgets = {
            'video_file': forms.ClearableFileInput(attrs={'accept': 'video/*'})
        }

    def clean_video_file(self):
        video = self.cleaned_data.get('video_file')
        if video:
            mime_type, _ = mimetypes.guess_type(video.name)
            if not mime_type or not mime_type.startswith('video'):
                raise ValidationError("Only video files are allowed.")
        return video

class VideoAdmin(admin.ModelAdmin):
    form = VideoAdminForm
    list_display = ['title', 'username', 'created_at']


admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Video, VideoAdmin)
