# -*- coding: utf-8 -*-
from django.db import models
import django.contrib.auth.models as auth_models

# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name
    
class Member(auth_models.User):
    picture = models.ImageField(upload_to="./images/user", null=True, blank=True)
    board = models.ForeignKey(Board)
    date_removal = models.DateTimeField(null=True, blank=True)
    is_in_board_of_directors = models.BooleanField()
    
    def __unicode__(self):
        return self.first_name + " " + self.last_name