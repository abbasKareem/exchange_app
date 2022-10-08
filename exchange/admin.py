from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    model = CustomUser
    search_fields = ('phone', 'username')
    list_filter = ('is_staff', 'start_date')
    ordering = ('-start_date',)
    list_display = ('email', 'phone', 'username', 'is_active',
                    'is_staff', 'id')
    fieldsets = (
        (None, {'fields': ('phone', 'username',
         'first_name', 'last_name', 'email', 'start_date')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'username', 'password1', 'password2',  'is_staff', 'first_name', 'last_name', 'email')}
         ),
    )


admin.site.register(CustomUser, UserAdminConfig)
