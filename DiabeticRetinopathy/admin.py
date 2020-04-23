from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from DiabeticRetinopathy.forms import RegisterForm
from DiabeticRetinopathy.models import *

# Register your models here.
class user_admin(UserAdmin):

    add_form = RegisterForm

    list_display = ('user_id','first_name','last_name','oname', 'email','bdate', 'staff','admin')
    search_fields = ('user_id', 'email', 'staff','admin')
    list_filter = ('user_id', 'email')
    ordering = ('first_name',)
    filter_horizontal = ()

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name','oname','bdate')}),
        ('Permissions', {'fields': ('admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )

admin.site.register(User, user_admin)

admin.site.register(Report)