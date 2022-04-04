from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import CustomUser
from .forms import RegisterForm, LogInForm, editprofileform
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from .tokens import account_activation_token
# Create your views here.


from django.views import generic
from django.urls import reverse_lazy
CustomUser = get_user_model()

def log_in(request):
    error = False
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user: 
                login(request, user)  
                return redirect('/')
            else: 
                error = True
    else:
        form = LogInForm()

    return render(request, 'account/login.html', {'form': form, 'error': error})




def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        # print(form.errors.as_data())
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('account/activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = RegisterForm()
    return render(request, 'account/register.html', {'form': form})



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('account:active')
    else:
        return HttpResponse('Activation link is invalid!')

def active(request):
    return render(request, 'account/confirmation_page.html')


def edit_profile(request, id):
    error = False
    if request.user.is_authenticated:
        user = get_object_or_404(CustomUser, id = id)
        form = editprofileform(request.POST, instance = user)
        if request.method == "POST":   
            if form.is_valid():
                form.save()  
                return redirect('app:profile', id = user.id)
            else: 
                error = True
        else: 
            form = editprofileform()
        return render(request, 'account/edit_profile.html', {'form': form, 'error': error})

class passwordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('app:index')
