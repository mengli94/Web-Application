# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.
class Post(models.Model):
    text = models.CharField(max_length=42)
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.text
    
class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    age = models.IntegerField()
    bio = models.CharField(max_length=420, default="Write your short bio here.", blank=True)
    picture = models.ImageField(upload_to="profile_pictures", default = "", blank=True)
    follows = models.ManyToManyField(User, related_name='follows')
    
    def __unicode__(self):
        return self.user

    @staticmethod
    def get_profile(user):
        try:
            profile = Profile.objects.get(user=user)
        except ObjectDoesNotExist:
            print("This profile does not exist.")

        return profile