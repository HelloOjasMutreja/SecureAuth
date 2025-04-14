from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login
from django.http import HttpResponse
from .utils import send_verification_email, verify_token
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_verification_email(user)
            return HttpResponse("Check your email to verify your account.")
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def verify_email(request, token):
    user_id = verify_token(token)
    if not user_id:
        return HttpResponse("Invalid or expired token.")
    user = User.objects.get(pk=user_id)
    user.is_verified = True
    user.is_active = True
    user.save()
    login(request, user)
    return HttpResponse("Email verified and you're now logged in.")
