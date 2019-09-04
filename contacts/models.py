from django.db import models
import contacts_django_rest_api.settings as settings

path = settings.MEDIA_ROOT


class ContactDetail(models.Model):
    owner = models.ForeignKey('auth.User', related_name='contact_details', on_delete=models.CASCADE)
    name = models.CharField(max_length=32, blank=False)
    email = models.EmailField(blank=False)
    image = models.ImageField(upload_to=path + "\\images", default=path + "\\default.png", blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(ContactDetail, self).save(*args, **kwargs)


class ContactNumber(models.Model):
    contact = models.ForeignKey(ContactDetail, related_name='contact_numbers', on_delete=models.CASCADE)
    number = models.CharField(max_length=10, blank=False)

    class Meta:
        ordering = ('contact__name',)

    def save(self, *args, **kwargs):
        super(ContactNumber, self).save(*args, **kwargs)
