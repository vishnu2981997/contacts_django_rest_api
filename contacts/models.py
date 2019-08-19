from django.db import models


class Contact(models.Model):
    owner = models.ForeignKey('auth.User', related_name='contacts', on_delete=models.CASCADE)
    name = models.CharField(max_length=32, unique=True, blank=False)
    email = models.EmailField(unique=True, blank=False)
    number = models.IntegerField(blank=False)
    file = models.FileField(blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Contact, self).save(*args, **kwargs)
