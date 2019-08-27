from material.admin.options import MaterialModelAdmin
from material.admin.sites import site
from .models import *


class ContactAdmin(MaterialModelAdmin):
    list_display = ("name", "email", "image", "created", "owner")
    list_filter = ["name", "email", "created", "owner__username"]
    search_fields = ["name", "email", "owner__username"]


site.register(Contact, ContactAdmin)
