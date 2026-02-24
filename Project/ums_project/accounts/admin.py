from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib import admin
admin.site.site_header = "UMS Administration"
admin.site.site_title = "UMS Admin Portal"
admin.site.index_title = "Welcome to UMS Admin Dashboard"


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'user_type', 'reg_no', 'semester', 'is_staff']
    list_filter = ['user_type', 'semester', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('user_type', 'reg_no', 'semester')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('user_type', 'reg_no', 'semester')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
