from __future__ import unicode_literals
from django.db import models

from apps.login_app.models import Users

class MessageManager(models.Manager):
    def message_validator(self, postData):
        errors = {}
        if len(postData['content']) < 1:
            errors['length'] = "Cannot post a blank message!"
        return errors

class Messages(models.Model):
    content = models.TextField()
    message_owner = models.ForeignKey(Users, related_name = 'owned_messages')
    message_receiver = models.ForeignKey(Users, related_name = 'received_messages')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = MessageManager()

class CommentManager(models.Manager):
    def comment_validator(self, postData):
        errors = {}
        if len(postData['content']) < 1:
            errors['length'] = "Cannot post a blank comment!"
        return errors

class Comments(models.Model):
    content = models.TextField()
    related_message = models.ForeignKey(Messages, related_name = 'comments')
    comment_owner = models.ForeignKey(Users, related_name = 'comments')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = CommentManager()


