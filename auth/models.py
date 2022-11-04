from django.contrib.auth.models import User
from django.db import models


class CustomUser(User):
    username = models.CharField(blank=True, null=True, verbose_name='Имя пользователя', max_length=100)
    publicKey = models.CharField(verbose_name='Публичный ключ', max_length=100)
    savedAssets = models.JSONField(null=True, blank=True, verbose_name='Избранные активы')

    class Meta:
        proxy = True
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super(CustomUser, self).save(*args, **kwargs)
