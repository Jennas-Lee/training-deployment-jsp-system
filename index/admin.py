from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from index.forms import UserChangeForm, UserCreationForm
from index.models import User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('number', 'name', 'submit', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('number', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_admin', 'submit')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('number', 'name', 'submit', 'password1', 'password2')
        }),
    )
    search_fields = ('number',)
    ordering = ('number',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
