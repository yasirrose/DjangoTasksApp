# Generated by Django 3.2 on 2021-04-14 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('Title', models.CharField(max_length=255)),
                ('Description', models.TextField()),
                ('Status', models.CharField(choices=[('1', 'Completed'), ('0', 'Pending')], max_length=20)),
                ('CreationDate', models.DateTimeField(auto_now_add=True)),
                ('DueDate', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('FirstName', models.CharField(max_length=128, null=True)),
                ('LastName', models.CharField(max_length=255, null=True)),
                ('Email', models.EmailField(max_length=254)),
                ('Password', models.CharField(max_length=255)),
                ('DateOfBirth', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='UserTasks',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('task', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='tasks.task')),
                ('user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='tasks.user')),
            ],
        ),
    ]
