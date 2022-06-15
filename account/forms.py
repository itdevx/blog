from django import forms
from django.core import validators
from django.contrib.auth import get_user_model
from account.models import User as U
from django.contrib.auth.forms import UserCreationForm
from main.models import Post


User = get_user_model()

class SingupForm(UserCreationForm):
    email = forms.EmailField(max_length=200)
    class Meta:
        model = U
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'id':'username' , 'class': 'form-control', 'placeholder':'نام خودرا وارد کنید'})
        self.fields['email'].widget.attrs.update({'id':'email', 'class': 'form-control', 'placeholder':'ایمیل خودرا وارد کنید'})
        self.fields['password1'].widget.attrs.update({'id':'password1', 'class': 'form-control', 'placeholder':'گذروازه را وارد کنید'})
        self.fields['password2'].widget.attrs.update({'id':'password2', 'class': 'form-control', 'placeholder':'تایید گذرواژه'})

    def clean_UserName(self):
        Username = self.cleaned_data.get('UserName')
        filtering = User.objects.filter(username=Username)
        if filtering.exists():
            raise forms.ValidationError('این نام کاربری وجود دارد')
        return Username

    def clean_Email(self):
        Email = self.cleaned_data.get('Email')
        filtering = User.objects.filter(email=Email)
        if filtering.exists():
            raise forms.ValidationError('با این ایمیل قبلا ثبت نام شده است')
        return Email

    def clean_Confirm_Password(self):
        data = self.cleaned_data
        p1 = self.cleaned_data.get('Password')
        p2 = self.cleaned_data.get('Confirm_Password')

        if p1 and p2:
            if p1 != p2:
                raise forms.ValidationError('رمز عبور فرق میکند')
            if len(p1) < 8:
                raise forms.ValidationError('رمز عبور نباید کمتر از 8 کاراکتر باشد')
        return data



class SinginForm(forms.Form):
    UserName = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'نام خودرا وارد کنید...', 'id':'username'}))
    Password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'رمز خودرا وارد کنید...', 'id':'password'}))



class CreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'author', 'description', 'status', 'categories', 'tags', 'intro_image']



class ProfileUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control', 'aria-describedby':'inputGroupPrepend2'})
        self.fields['email'].widget.attrs.update({'class':'form-control'})
        self.fields['first_name'].widget.attrs.update({'class':'form-control'})
        self.fields['last_name'].widget.attrs.update({'class':'form-control'})
        self.fields['image'].widget.attrs.update({'class':'form-control'})
        self.fields['info'].widget.attrs.update({'class':'form-control'})
        self.fields['job'].widget.attrs.update({'class':'form-control', 'placeholder':'به طور مثال : متخصص SEO'})
        self.fields['linkedin'].widget.attrs.update({'class':'form-control'})
        self.fields['twitter'].widget.attrs.update({'class':'form-control'})
        self.fields['instagram'].widget.attrs.update({'class':'form-control'})
        self.fields['github'].widget.attrs.update({'class':'form-control'})
        self.fields['telegram'].widget.attrs.update({'class':'form-control'})
        self.fields['website'].widget.attrs.update({'class':'form-control'})

        if not user.is_superuser:
            self.fields['username'].disabled = True
            self.fields['email'].disabled = True

    class Meta:
        model = U
        fields = ['username', 'email', 'first_name', 'last_name', 'image', 'job', 'info', 'linkedin', 'twitter', 'instagram', 'github', 'telegram', 'website']



class UsersEditForm(forms.ModelForm):
    class Meta:
        model = U
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UsersEditForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

