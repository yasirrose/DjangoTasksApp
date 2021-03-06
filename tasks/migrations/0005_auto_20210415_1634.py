# Generated by Django 3.2 on 2021-04-15 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_auto_20210415_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertasks',
            name='task',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='task', to='tasks.task'),
        ),
        migrations.AlterField(
            model_name='usertasks',
            name='user',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
