from django.db import migrations, models


def forwards(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('blog', 'Profile')

    for user in User.objects.all():
        Profile.objects.get_or_create(user=user)


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='username',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.RunPython(forwards),
    ]
