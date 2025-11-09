from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активный сотрудник',
        help_text='Определяет, имеет ли пользователь доступ к API'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username