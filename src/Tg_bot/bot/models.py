from django.db import models

class User(models.Model):
    external_id = models.PositiveIntegerField(verbose_name="id в соц сети", unique=True)

    class Meta:
        verbose_name = 'Юзер'
