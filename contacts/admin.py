from django.contrib import admin
from .models import *


# Register your models here.


class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "number", "file", "created", "owner")
    list_filter = ["name", "email", "number", "created", "owner"]
    search_fields = ["name", "email", "number"]


admin.site.register(Contact, ContactAdmin)
