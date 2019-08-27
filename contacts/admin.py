from django.contrib import admin
from .models import *


# Register your models here.


class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "image", "created", "owner")
    list_filter = ["name", "email", "created", "owner__username"]
    search_fields = ["name", "email", "owner__username"]

    # @staticmethod
    # def numbers(obj):
    #     numbers = MobileNumber.objects.filter(contact=obj.id)
    #     if numbers:
    #         return " ".join(str(i.number) for i in numbers)
    #     else:
    #         return None


admin.site.register(Contact, ContactAdmin)
