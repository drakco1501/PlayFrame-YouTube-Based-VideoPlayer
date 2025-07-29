from django.shortcuts import render, redirect
from django.contrib import messages


from accounts.models import *
from accounts.forms import *
from accounts.views import user_login_required


from django.shortcuts import get_object_or_404, render

import os
from django.http import FileResponse


from django.db.models import Q

from django.db.models import Q

def home(request):
    search_query = request.GET.get('search', '')

    if search_query:
        videos = Video.objects.filter(
            Q(title__icontains=search_query) |
            Q(username__username__icontains=search_query)
        ).order_by('?')[:10]
    else:
        videos = Video.objects.order_by('?')[:10]

    is_logged = request.session.get('is_logged_in', False)
    context = {'is_logged': is_logged, 'videos': videos}

    if is_logged:
        userid = request.session['user_id']
        user = CustomUser.objects.get(id=userid)
        profile = Profile.objects.get(user=user)
        context['profile'] = profile

    return render(request, 'dashboard/home.html', context)

@user_login_required
def profile(request):
    userid = request.session['user_id']  
    user = CustomUser.objects.get(id = userid)
    profile = Profile.objects.get(user = user) 
    videos = user.videos.all() 
    context = {
        'profile' : profile,
        'videos' : videos,
    } 
    return render(request, 'dashboard/profile.html', context)


@user_login_required
def update_profile(request):
    try:
        userid = request.session['user_id']  
        user = CustomUser.objects.get(id = userid)
        profile = Profile.objects.get(username = user.username) 
    except Profile.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect('dashboard:home')

    if request.method == 'POST':
        if 'remove_image' in request.POST:
            # Reset the profile image to default
            profile.profile_image = 'profiles/default.png'
            profile.save()
            messages.success(request, "Profile image has been reset to default.")
            return redirect('dashboard:profile')

        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('dashboard:profile')
    else:
        form = ProfileForm(instance=profile)

    context = {
        'profile': profile,
        'form': form,
    }
    return render(request, 'dashboard/update_profile.html', context)

@user_login_required
def upload_video(request): 
    userid = request.session['user_id']  
    user = CustomUser.objects.get(id=userid)

    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)  # include request.FILES for file uploads
        if form.is_valid():
            video = form.save(commit=False)  # don't save yet
            video.username = user
            video.save()
            return redirect('dashboard:profile')
    else:
        form = VideoForm()
    
    context = {
        'form': form,
    }
    return render(request, 'dashboard/upload_vds.html', context)

@user_login_required
def edit_vds(request, id):
    video = Video.objects.get(id = id) 
    if request.method == 'POST':
        form = VideoForm(request.POST , instance=video)
        if form.is_valid():
            form.save()
            return redirect('dashboard:profile')
    else:
        form = VideoForm(instance=video)
    context = {
        'form' : form,
        'video' : video,
    }
    return render(request, 'dashboard/edit_vds.html', context)

@user_login_required
def delete_vds(request, id):
    video = get_object_or_404(Video, id=id)
    if request.method == 'POST':
        video.delete()
        return redirect('dashboard:profile')
    context = {
        'video': video,
    }
    return render(request, 'dashboard/confirm_delete.html', context)







def video_play(request, id):
    video = get_object_or_404(Video, id=id)
    user = video.username 
    profile = Profile.objects.get(user=user)
    suggestions = Video.objects.exclude(id=id).order_by('?')[:6]
    src = "{{}}"
    context = {
        'video': video,
        'suggestions': suggestions, 
        'profile': profile,
    }
    return render(request, 'dashboard/video_play.html', context)
