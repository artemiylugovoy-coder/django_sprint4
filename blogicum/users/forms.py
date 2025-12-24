# users/forms.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from blog.models import Profile
from django.utils import timezone
# Получаем модель пользователя:
User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="Имя")
    last_name = forms.CharField(max_length=30, required=True, label="Фамилия")
    email = forms.EmailField(max_length=254,
                             required=True,
                             label="Электронная почта"
                             )
    get_full_name = f'{first_name} {last_name}'

    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'password1',
                  'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()  # Сохраняем пользователя

        # Если профиль не существует, создаем новый (это походу надо убрать)
        profile, created = Profile.objects.get_or_create(user=user,
                                                         date_joined=timezone
                                                         .now())
        profile.get_full_name = f"{user.first_name} {user.last_name}"
        if commit:
            profile.save()  # Сохраняем профиль

        return user
