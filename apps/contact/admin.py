from django.contrib import admin

from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    search_fields = ("full_name", 'phone_number')
    list_display = ["full_name", 'phone_number', 'is_published', 'created_at']
    readonly_fields = ("created_at", 'updated_at')
    # filter_vertical = ("is_published", )
    list_filter = ("is_published", )

admin.site.register(Contact, ContactAdmin)
