from django.shortcuts import render, redirect, HttpResponseRedirect
# password reset
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.tokens import default_token_generator
from django.views.generic.edit import FormView
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import resolve_url
from django.core.exceptions import ValidationError
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import (
    PasswordResetForm,
    SetPasswordForm,
    PasswordChangeForm
)
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from extentions.utils import jalali_converter
from django.http import Http404
from django.views import View
from django.views.generic import (
    UpdateView,
    DeleteView,
    CreateView
)
from account.mixins import (
    FormValidMixins,
    FieldsMixins,
    SuperuserAccessMixins,
    SuperAccessUpdateUsers,
    SuperuserAccessDeleteUserMixins
)
from account.forms import (
    SinginForm,
    SingupForm,
    ProfileUpdateForm,
    UsersEditForm
)
from django.contrib.auth import (
    login,
    logout,
    authenticate
)

# Email
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from account.models import User
from main.models import Post 
from django.core.paginator import Paginator



UserModel = get_user_model()

class DashboardHome(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                posts = Post.objects.all().order_by('-id')
                paginator = Paginator(posts, 10)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
            else:
                posts = Post.objects.filter(author=request.user).order_by('-id')
                paginator = Paginator(posts, 10)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
        else:
            return redirect('account:login')
        c = {
            'posts':page_obj
        }
        return render(request, 'ViewsAccount/index.html', c)



class DeleteUserView(SuperuserAccessDeleteUserMixins, DeleteView):
    model = User
    template_name = 'ViewsAccount/delete-user.html'
    context_object_name = 'user'
    success_url = reverse_lazy('account:all-user')



class AllUserView(View):
    def get(self, request):
        if request.user.is_superuser:
            users = User.objects.values().order_by('-id')
            paginator = Paginator(users, 20)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        else:
            raise Http404('Page not found!')
        context = {
            'users':page_obj
        }
        return render(request, 'ViewsAccount/all-user.html', context)



def login_view(request):
    if request.user.is_authenticated:
        return redirect('main:home')
    else:
        form = SinginForm(request.POST or None)
        if form.is_valid():
            Username = form.cleaned_data.get('UserName')
            Password = form.cleaned_data.get('Password')
            user = authenticate(request, username=Username, password=Password)
            if user is not None:
                # if user.is_superuser or user.is_author:
                #     login(request, user)
                #     return redirect('account:home')
                # else:
                login(request, user)
                return redirect('account:home')
            else:
                form.add_error('UserName', 'نام کاربری یا کلمه عبور اشتباه میباشد')
        c = {
            'form':form
        }
    return render(request, 'ViewsAccount/auth_login_boxed.html', c)



class Register(CreateView):
    template_name = 'ViewsAccount/auth_register_boxed.html'
    form_class = SingupForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'فعال سازی اکانت'
        message = render_to_string('ViewsAccount/acc_verify_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="utf-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, shrink-to-fit=no">
                <title>ایمیل فعال سازی</title>
                <link rel="icon" type="image/x-icon" href="assets/img/favicon.ico">
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
                <!-- BEGIN GLOBAL MANDATORY STYLES -->
            </head>
            <body dir="rtl" class="form" style="background: #1a1a1a; color: #888ea8;" >
                <style>
                    ::selection {
                        background: transparent;
                        color: #009688;
                    }
                    body {
                        height: 100%;
                        overflow: auto;
                        margin: 0;
                        padding: 0;
                        background-color: #1e1e1e;
                    }
                    .form-form .form-container .form-content {
                        display: block;
                        width: 100%;
                        padding: 25px;
                        border: 1px solid #000;
                        text-align: center;
                        border-radius: 15px;
                        box-shadow: 0 6px 10px 0 rgb(0 0 0 / 14%), 0 1px 18px 0 rgb(0 0 0 / 12%), 0 3px 5px -1px rgb(0 0 0 / 20%);
                    }        
                    .form-form .form-container {
                        align-items: center;
                        display: flex;
                        flex-grow: 1;
                        width: 100%;
                        min-height: 100%;
                    }
                    .form-form {
                        width: 50%;
                        display: flex;
                        flex-direction: column;
                        min-height: 100%;
                        margin: 0 auto;
                    }
                    .form-form .form-form-wrap {
                        max-width: 480px;
                        margin: 0 auto ;
                        /* margin-right: 980px; */
                        min-width: 311px;
                        min-height: 100%;
                        align-self: center;
                        width: 100%;
                        height: 100vh;
                        justify-content: center;
                    }
                    ::selection {
                        background: transparent;
                        color: #009688;
                    }
                </style>
                <div class="form-container outer">
                    <div class="form-form">
                        <div class="form-form-wrap">
                            <div class="form-container">
                                <div class="form-content">
                                    <h3 class="m-5">ایمیل فعالسازی</h3>
                                    <p>
            لینک فعال ساز برای شما ارسال شد لطفا ایمیلتان را چک کنید
                                    </p>
                                </div>                    
                            </div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
        ''')

def verify(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="utf-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, shrink-to-fit=no">
                <title>ثبت حساب کاربری</title>
                <link rel="icon" type="image/x-icon" href="assets/img/favicon.ico">
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
                <!-- BEGIN GLOBAL MANDATORY STYLES -->
            </head>
            <body dir="rtl" class="form" style="background: #1a1a1a; color: #888ea8;" >
                <style>
                    ::selection {
                        background: transparent;
                        color: #009688;
                    }
                    body {
                        height: 100%;
                        overflow: auto;
                        margin: 0;
                        padding: 0;
                        background-color: #1e1e1e;
                    }
                    .form-form .form-container .form-content {
                        display: block;
                        width: 100%;
                        padding: 25px;
                        border: 1px solid #000;
                        text-align: center;
                        border-radius: 15px;
                        box-shadow: 0 6px 10px 0 rgb(0 0 0 / 14%), 0 1px 18px 0 rgb(0 0 0 / 12%), 0 3px 5px -1px rgb(0 0 0 / 20%);
                    }        
                    .form-form .form-container {
                        align-items: center;
                        display: flex;
                        flex-grow: 1;
                        width: 100%;
                        min-height: 100%;
                    }
                    .form-form {
                        width: 50%;
                        display: flex;
                        flex-direction: column;
                        min-height: 100%;
                        margin: 0 auto;
                    }
                    .form-form .form-form-wrap {
                        max-width: 480px;
                        margin: 0 auto ;
                        /* margin-right: 980px; */
                        min-width: 311px;
                        min-height: 100%;
                        align-self: center;
                        width: 100%;
                        height: 100vh;
                        justify-content: center;
                    }
                    a{
                        color: #009688;
                        border-bottom: 1px solid;
                    }
                    ::selection {
                        background: transparent;
                        color: #009688;
                    }
                </style>

                <div class="form-container outer">
                    <div class="form-form">
                        <div class="form-form-wrap">
                            <div class="form-container">
                                <div class="form-content">
                                    <p>
                                        حساب کاربری شما با موفقیت ثبت شد برای ورود بر روی لینک زیر کلیک کنید
                                    </p>
                                    <a href="/">ورود به صفحه اصلی</a>
                                </div>                    
                            </div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
        ''')
    else:
        return HttpResponse('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="utf-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, shrink-to-fit=no">
                <title>لینک منقضی شد</title>
                <link rel="icon" type="image/x-icon" href="assets/img/favicon.ico">
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
                <!-- BEGIN GLOBAL MANDATORY STYLES -->
            </head>
            <body dir="rtl" class="form" style="background: #1a1a1a; color: #888ea8;" >
                <style>
                    ::selection {
                        background: transparent;
                        color: #009688;
                    }
                    body {
                        height: 100%;
                        overflow: auto;
                        margin: 0;
                        padding: 0;
                        background-color: #1e1e1e;
                    }
                    .form-form .form-container .form-content {
                        display: block;
                        width: 100%;
                        padding: 25px;
                        border: 1px solid #000;
                        text-align: center;
                        border-radius: 15px;
                        box-shadow: 0 6px 10px 0 rgb(0 0 0 / 14%), 0 1px 18px 0 rgb(0 0 0 / 12%), 0 3px 5px -1px rgb(0 0 0 / 20%);
                    }       
                    .form-form .form-container {
                        align-items: center;
                        display: flex;
                        flex-grow: 1;
                        width: 100%;
                        min-height: 100%;
                    }
                    .form-form {
                        width: 50%;
                        display: flex;
                        flex-direction: column;
                        min-height: 100%;
                        margin: 0 auto;
                    }
                    .form-form .form-form-wrap {
                        max-width: 480px;
                        margin: 0 auto ;
                        /* margin-right: 980px; */
                        min-width: 311px;
                        min-height: 100%;
                        align-self: center;
                        width: 100%;
                        height: 100vh;
                        justify-content: center;
                    }
                    a{
                        color: #009688;
                        border-bottom: 1px solid;
                    }
                </style>
                <div class="form-container outer">
                    <div class="form-form">
                        <div class="form-form-wrap">
                            <div class="form-container">
                                <div class="form-content">
                                    <p class="text-danger">
                                       لینک فعال سازی منقضی شده است
                                    </p>
                                </div>                    
                            </div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
        
        ''')



def logout_request(request):
    logout(request)
    return redirect('main:home')



class CreatePostView(FormValidMixins, FieldsMixins, CreateView):
    model = Post
    success_url = reverse_lazy('account:home')
    template_name = 'dash/create.html'



class UpdatePostView(FieldsMixins, UpdateView):
    model = Post
    success_url = reverse_lazy('account:home')
    template_name = 'dash/create.html'



class DeletePostView(SuperuserAccessMixins, DeleteView):
    model = Post
    template_name = 'dash/delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('account:home')




class ProfileUpdate(UpdateView):
    model = User
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('account:home')
    template_name = 'dash/update_profile.html'

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(ProfileUpdate, self).get_form_kwargs()
        kwargs.update({
            'user':self.request.user
        })
        return kwargs



class EditUsersView(SuperAccessUpdateUsers, UpdateView):
    model = User
    form_class = UsersEditForm
    template_name = 'dash/update_users.html'
    success_url = reverse_lazy('account:all-user')



# password Reset
class PasswordContextMixin:
    extra_context = None
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"title": self.title, **(self.extra_context or {})})
        return context



class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = "register/password_reset_email.html"
    extra_email_context = None
    # add class form-control in PasswordRestForm in form file
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = "register/password_reset_subject.txt"
    success_url = reverse_lazy("account:password_reset_done")
    template_name = "register/password_reset_form.html"
    title = _("Password reset")
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            "use_https": self.request.is_secure(),
            "token_generator": self.token_generator,
            "from_email": self.from_email,
            "email_template_name": self.email_template_name,
            "subject_template_name": self.subject_template_name,
            "request": self.request,
            "html_email_template_name": self.html_email_template_name,
            "extra_email_context": self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)



INTERNAL_RESET_SESSION_TOKEN = "_password_reset_token"



class PasswordResetConfirmView(PasswordContextMixin, FormView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    reset_url_token = "set-password"
    success_url = reverse_lazy("account:password_reset_complete")
    template_name = "register/password_reset_confirm.html"
    title = _("Enter new password")
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        if "uidb64" not in kwargs or "token" not in kwargs:
            raise ImproperlyConfigured(
                "The URL path must contain 'uidb64' and 'token' parameters."
            )

        self.validlink = False
        self.user = self.get_user(kwargs["uidb64"])

        if self.user is not None:
            token = kwargs["token"]
            if token == self.reset_url_token:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(
                        token, self.reset_url_token
                    )
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
            try:
                # urlsafe_base64_decode() decodes to bytestring
                uid = urlsafe_base64_decode(uidb64).decode()
                user = UserModel._default_manager.get(pk=uid)
            except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist, ValidationError):
                user = None
            return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context['validlink'] = True
        else:
            context.update({
                'form': None,
                'title': _('Password reset unsuccessful'),
                'validlink': False,
            })
        return context



class PasswordResetDoneView(PasswordContextMixin, TemplateView):
    template_name = "register/password_reset_done.html"
    title = _("Password reset sent")



class PasswordResetCompleteView(PasswordContextMixin, TemplateView):
    template_name = "register/password_reset_complete.html"
    title = _("Password reset complete")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_url"] = resolve_url(settings.LOGIN_URL)
        return context



class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("account:home")
    template_name = "register/change-password.html"
    title = _("Password change")

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)
