from django.shortcuts import render, redirect
from . forms import CreateUserForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,  urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.forms import PasswordResetForm


def homepage(request):
    messages_to_display = messages.get_messages(request)

    return render(request, 'auth_app/index.html', {"messages": messages_to_display})



def register(request):

    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit = False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = "Activate your GrinDorms account"
            message = render_to_string("auth_app/account_activation_email.html",{ 
                "user":user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user)
            })
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, "Please check your email to complete the registration process. It might be in your spam folder.")

            return redirect("")

    return render(request, 'auth_app/register.html', {"registerform":form})



def my_login(request):

    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:

                    auth.login(request, user)
                    return redirect("dashboard")
                else:
                    messages.error(request, "Your account is not activated. Please check your email to activate your account.")
                    return redirect("my-login")
    
    context = {'loginform':form}

    return render(request, 'auth_app/my-login.html', context=context)


@login_required(login_url="my-login")
def dashboard(request):

    return render(request, 'auth_app/dashboard.html')


def user_logout(request):

    auth.logout(request)

    return redirect("")


def activate(request, uidb64, token):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        login(request, user)

        return redirect(reverse("my-login"))
    else:
        messages.error(request, "Activation link is invalid or expired.")
        return redirect("")


# def password_reset(request):
#     form = ResetPasswordForm()

#     if request.method == "POST":

#         form = ResetPasswordForm(request, data=request.POST)
    
#     context = {'passwordresetform':form}

#     return render(request, 'auth_app/templates/registration/password_reset_form.html', context=context)
#     return redirect("my-login")

