from django.urls import path
from .views import *

app_name = 'dashboard'

urlpatterns = [
    path('', home , name='home'),
    path('profile', profile , name='profile'),
    path('update_profile', update_profile , name='update_profile'),
    path('video/<uuid:id>/', video_play, name='video_play'),
    path('upload/video', upload_video, name="upload_vds"),
    path('edit_vds/<uuid:id>', edit_vds, name="edit_vds"),
    path('delete_vds/<uuid:id>', delete_vds, name="delete_vds"),
]

