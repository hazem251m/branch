from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django import forms
from .models import User



class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(max_length=64,label='password',widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=64,label='password2',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password','email')
    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("كلمات المرور غير متطابقة ")
        return password2
    
    def save(self , commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model =User
        fields = ['username','email', 'password', 'role', 'is_active', 'is_admin', 'debet']

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    create_form = UserCreationForm
    list_display = ('username','email', 'role', 'debet')
    list_filter = ('username', 'role',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name',)}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Credit Info', {'fields': ('debet', )}),
        ('Role Info', {'fields': ('role', )}),
    )
    


admin.site.register(User, UserAdmin)