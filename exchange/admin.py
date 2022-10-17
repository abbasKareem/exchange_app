from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from datetime import datetime, timezone
from django.utils import timesince
from django.http import HttpResponse
import csv
from django.contrib.admin.views.main import ChangeList


def export_as_csv(self, request, queryset):
    meta = self.model._meta
    field_names = [field.name for field in meta.fields]
    response = HttpResponse(content_type='text.csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
        meta)
    writer = csv.writer(response)
    writer.writerow(field_names)
    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])
    return response


export_as_csv.short_description = "Download Payment"


class UserAdminConfig(UserAdmin):
    model = CustomUser
    search_fields = ('phone',)
    list_filter = ('is_staff', 'start_date')
    ordering = ('-start_date',)
    list_display = ('email', 'phone', 'is_active',
                    'is_staff', 'id')
    fieldsets = (
        (None, {'fields': ('phone',
         'first_name', 'last_name', 'email', 'start_date')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2',  'is_staff', 'first_name', 'last_name', 'email')}
         ),
    )


class TypeAdmin(admin.ModelAdmin):

    list_display = ['type_name', 'is_public']


class TranscationAdmin(admin.ModelAdmin):
    list_display = ['show_details', 'tran_from', 'tran_to', 'amount']

    def show_details(self, obj):
        return "View"



class PaymentAdmin(admin.ModelAdmin):
    readonly_fields = ['total', 'transcation',  'user', 'create_at', 'hawala_number',
                       'mac_in', 'mac_out', 'recvied_amount']
    list_display = ['status', 'user', 'create_at', 'phone',
                    'recvied_amount', 'total', 'transcation', 'since']

 
    list_filter = ['status', 'create_at', 'transcation']
    list_per_page = 3
    # save_as = True
    # save_on_top = True
    change_list_template = 'change_list_payment.html'
    actions = [export_as_csv]

      

    def phone(self, obj):
        return obj.user.phone

    def since(self, obj):
        date_time_dif = datetime.now(timezone.utc) - obj.create_at
        return str(date_time_dif)[:-6] + ' ago'



admin.site.register(CustomUser, UserAdminConfig)
admin.site.register(Type, TypeAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Transcation, TranscationAdmin)

# admin.site.register(Notification)
# admin.site.register(OneSignal)
