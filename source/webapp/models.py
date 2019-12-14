from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Foto(models.Model):
    foto = models.ImageField(null=False, blank=False, upload_to='user_pics', verbose_name='Фото')
    subscribe = models.CharField(max_length=50, verbose_name='Подпись', null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    rating = models.IntegerField(default=0, verbose_name='Лайки')
    user = models.ForeignKey(User, related_name='profile', on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.user.get_full_name() + "'s User"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Comments(models.Model):
    text = models.TextField(max_length=400, null=True, blank=True, verbose_name='Текст')
    fotocomment = models.ForeignKey(Foto, related_name='comment_foto', verbose_name='Фото', on_delete=models.CASCADE)
    author = models.ForeignKey(User, null=False, blank=False, related_name='comment_profile', on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return str(self.text)
