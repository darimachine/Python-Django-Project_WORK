# Generated by Django 4.2.2 on 2023-06-22 17:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pet',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='pet',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='pet',
            unique_together={('user', 'name')},
        ),
        migrations.RemoveField(
            model_name='pet',
            name='user_profile',
        ),
    ]
