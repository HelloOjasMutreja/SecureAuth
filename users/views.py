from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, get_backends
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from .utils import send_verification_email, verify_token
from .forms import CustomUserCreationForm
from django_otp.decorators import otp_required

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_verification_email(user)
            return HttpResponse("Check your email to verify your account.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def verify_email(request, token):
    user_id = verify_token(token)
    if not user_id:
        return HttpResponse("Invalid or expired token.")
    
    user = User.objects.get(pk=user_id)
    user.is_verified = True
    user.is_active = True
    user.save()

    # Set the backend manually since there are multiple
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)

    return HttpResponse("Email verified and you're now logged in.")

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

@otp_required
def dashboard(request):
    return HttpResponse("Secure dashboard!")