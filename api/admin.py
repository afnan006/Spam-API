from django.contrib import admin
from .models import User, Contact, SpamReport

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone_number', 'email')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'is_spam')

@admin.register(SpamReport)
class SpamReportAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'report_count', 'created_at')  # Do not include 'reported_by'
