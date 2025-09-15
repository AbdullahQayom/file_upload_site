from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import SignUpForm, SignInForm, FileUploadForm
from .models import File
from django.http import HttpResponse, Http404
from django.conf import settings
import os
from wsgiref.util import FileWrapper

#home 
def home(request):
    return render(request, 'core/base.html')

# Signup
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('upload_file')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})

#Signin
def signin_view(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('upload_file')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = SignInForm()
    return render(request, 'core/signin.html', {'form': form})

#Signout
def signout_view(request):
    logout(request)
    return redirect('home')

# File Upload
@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_obj = form.save(commit=False)
            file_obj.user = request.user
            file_obj.save()
            return redirect('my_files')
    else:
        form = FileUploadForm()
    return render(request, 'core/upload.html', {'form': form})

# My Files
@login_required
def my_files(request):
    files = File.objects.filter(user=request.user).order_by('-upload_date')
    return render(request, 'core/my_files.html', {'files': files})

# Public Files
def public_files(request):
    files = File.objects.filter(is_public=True).order_by('-upload_date')
    return render(request, 'core/public_files.html', {'files': files})

#Download File
def download_file(request, file_id):
    file_obj = get_object_or_404(File, pk=file_id)
    if not file_obj.is_public and file_obj.user != request.user:
        raise Http404("File does not exist or you don't have permission to download it.")
    
    file_path = os.path.join(settings.MEDIA_ROOT, file_obj.filepath.name)
    if os.path.exists(file_path):
        wrapper = FileWrapper(open(file_path, 'rb'))
        response = HttpResponse(wrapper, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file_obj.filename}"'
        return response
    else:
        raise Http404("File not found.")

#Delete File
@login_required
def delete_file(request, file_id):
    file_obj = get_object_or_404(File, pk=file_id)
    if file_obj.user == request.user:
        file_obj.delete()
    return redirect('my_files')
