# Generated by Django 2.2.1 on 2019-05-28 20:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0004_table_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tablegift',
            name='invite',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Invite'),
        ),
    ]
