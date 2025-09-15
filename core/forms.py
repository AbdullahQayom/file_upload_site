from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import File

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class SignInForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Password")


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['filename', 'filepath', 'is_public']

    def clean_filepath(self):
        file = self.cleaned_data.get('filepath')
        if file:
            # File limit 10 mb
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("File size cannot exceed 10 MB.")
            
            #file types
            allowed_types = [
                'application/pdf',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'image/jpeg',
                'image/png'
            ]
            if file.content_type not in allowed_types:
                raise forms.ValidationError("Invalid file type. Only PDF, DOCX, JPG, PNG are allowed.")
        return file
