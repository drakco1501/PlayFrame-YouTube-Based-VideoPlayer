from django import forms
from django.forms import ModelForm
from .models import *


from django.core.exceptions import ValidationError
import mimetypes

class CustomUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),  # Ensure password is masked
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Enter Username'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter Email Address'
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Enter Password'
        })

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email exists. Try another email")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image','username', 'email', 'short_intro', 'bio']


    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Enter Username'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter Email Address'
        })
        self.fields['short_intro'].widget.attrs.update({
            'placeholder': 'Add your work title Ex - videography, edits'
        })
        self.fields['bio'].widget.attrs.update({
            'placeholder': 'Add a short bio'
        })

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Profile.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Username is already taken")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Profile.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Email exists. Try another email")
        return email
    

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter video title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter video description',
                'rows': 3
            }),
            'video_file': forms.ClearableFileInput(attrs={
                'accept': 'video/*',
                'class': 'form-control'
            }),
        }

    def clean_video_file(self):
        video = self.cleaned_data.get('video_file')
        if video:
            mime_type, _ = mimetypes.guess_type(video.name)
            if not mime_type or not mime_type.startswith('video'):
                raise ValidationError("Only video files are allowed.")
        return video