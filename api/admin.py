from django.contrib import admin
from .models import Motagrat,Motagrat_Products,Products,User_Request,Control_Period

# Register your models here.

class ControlPeriodAdmin(admin.ModelAdmin):
    class Meta:
        model = Control_Period
        fields = '__all__'

admin.site.register(Motagrat)
admin.site.register(Motagrat_Products)
admin.site.register(Products)
admin.site.register(User_Request)
admin.site.register(Control_Period)