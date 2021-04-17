from django.db import models

# Create your models here
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime


from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    EmailField,
    ForeignKey,
    IntegerField,
    Model,
    OneToOneField,
    TextField,
    UniqueConstraint,
    UUIDField,
    AutoField,
    FileField,
)


# class User(AbstractUser):
#     date_of_birth = DateField()

class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE,related_name="profile")
    date_of_birth = DateField(null=False)

#
#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


class Task(Model):
    TASK_STATUSES = (("1", "Completed"), ("0", "Pending"))
    id = AutoField(primary_key=True)
    title = CharField(max_length=255, null=False)
    description = TextField(null=False)
    status = CharField(max_length=20, choices=TASK_STATUSES)
    creation_date = DateTimeField(auto_now_add=True)
    created_by = ForeignKey(User, on_delete=CASCADE)
    due_date = DateTimeField()

    def __str__(self):
        return self.id


class TaskUser(Model):
    id = AutoField(primary_key=True)
    user = ForeignKey(
        User, on_delete=CASCADE, db_constraint=False, related_name="users"
    )
    task = ForeignKey(Task, on_delete=CASCADE, db_constraint=False, related_name="tasks")

class VoiceNote(Model):
    id = AutoField(primary_key=True)
    voice_memo = FileField(upload_to='recordings')
    size = CharField(max_length=100,null=True, blank=True)
    duration = CharField(max_length=100, null=True, blank=True)
    creation_date = DateTimeField(auto_now_add=True)
    task = ForeignKey(Task, on_delete=CASCADE, db_constraint=False, related_name="task")
    user = ForeignKey(User, on_delete=CASCADE, db_constraint=False, related_name="user")

    # class Meta:
    #     db_table = "users_voicenotes"

    def to_dict_json(self):
        return {
            'voice_memo': self.voice_memo,
        }

