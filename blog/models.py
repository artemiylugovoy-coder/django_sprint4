# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from core.models import PublishedModel
from django.urls import reverse
from django.conf import settings

User = get_user_model()


class Post(PublishedModel):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(verbose_name='Дата и время публикации',
                                    help_text='Если установить дату и время в '
                                    'будущем — можно делать '
                                    'отложенные публикации.',
                                    )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор публикации'
                               )
    location = models.ForeignKey('Location',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 verbose_name='Местоположение'
                                 )
    category = models.ForeignKey('Category',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 verbose_name='Категория'
                                 )
    image = models.ImageField('Фото', upload_to='post_images', blank=True)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Category(PublishedModel):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(unique=True,
                            verbose_name='Идентификатор',
                            help_text='Идентификатор страницы для URL; '
                            'разрешены символы латиницы, цифры, '
                            'дефис и подчёркивание.'
                            )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(PublishedModel):
    name = models.CharField(max_length=256, verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Profile(models.Model):
    get_full_name = models.CharField(max_length=256, blank=True, null=True)
    date_joined = models.DateTimeField(verbose_name='Дата и время регистрации',
                                       auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True,
                                       verbose_name='Опубликовано',
                                       help_text='Снимите галочку, '
                                       'чтобы скрыть публикацию.'
                                       )
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='profile',
                                null=True)
    username = models.CharField(max_length=150, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.get_full_name:
            self.get_full_name = f"{self.user.first_name} {self.user.last_name}"
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Comment(PublishedModel):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор комментария'
                               )
    text = models.TextField(verbose_name='Текст')
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             null=True,
                             related_name='comments',
                             )