from django.contrib import admin

from .models import *


class ContactNumberAdmin(admin.StackedInline):
    model = ContactNumber
    show_change_link = True
    fields = ["contact", "number"]
    extra = 1
    # readonly_fields = ["contact"]


class ContactDetailAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "image", "created", "owner")
    list_filter = ["name", "email", "created", "owner__username"]
    search_fields = ["name", "email", "owner__username"]
    inlines = [ContactNumberAdmin, ]


class ContactNumberEditAdmin(admin.ModelAdmin):
    list_display = ("contact", "number")
    list_filter = ["contact__name", "number"]
    search_fields = ["contact__name", "number"]


admin.site.register(ContactDetail, ContactDetailAdmin)
admin.site.register(ContactNumber, ContactNumberEditAdmin)
