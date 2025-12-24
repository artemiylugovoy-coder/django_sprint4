from django import forms

# Импортируем класс модели Birthday.
from .models import Post, Category, Location, Comment, User, Profile
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.utils import timezone


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'pub_date', 'location', 'category', 'image')
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class ChangForm(forms.ModelForm):
    username = forms.CharField(max_length=30,
                               required=True,
                               label="Имя пользователя"
                               )
    first_name = forms.CharField(max_length=30,
                                 required=True,
                                 label="Имя"
                                 )
    last_name = forms.CharField(max_length=30,
                                required=True,
                                label="Фамилия"
                                )
    email = forms.EmailField(max_length=254,
                             required=True,
                             label="Электронная почта"
                             )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = self.instance  # Используем текущий экземпляр пользователя
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        # Обновляем или создаем профиль пользователя
        profile, created = Profile.objects.get_or_create(user=user)
        if commit:
            profile.save()

        return user
