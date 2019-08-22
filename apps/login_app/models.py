from __future__ import unicode_literals
from django.db import models
import datetime

class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        if 'first_name' in postData:
            if len(postData['first_name']) < 2:
                errors['first_name'] = "First name must be at least two characters long"
            elif len(postData['first_name']) > 30:
                errors['first_name'] = "Your name is waaaaay too long."
        if 'last_name' in postData:
            if len(postData['last_name']) < 2:
                errors['last_name'] = "Last name must be at least two characters long"
        if 'regPassword' in postData:
            if len(postData['regPassword']) < 8:
                errors['pw_length'] = "Password must be at least eight characters long"
            if postData['regPassword'] != postData['confPassword']:
                errors['pw_match'] = "Passwords do not match!"
        return errors

class Users(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255) 
    pw_hash = models.CharField(max_length = 255)
    desc = models.TextField(default = "")
    user_level = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()