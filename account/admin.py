from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    ordering = ['email']  # Make sure it orders by email now

    list_display = ['email', 'is_staff', 'is_active']
    search_fields = ['email', 'first_name', 'last_name']

admin.site.register(CustomUser, CustomUserAdmin)