# -*- coding: utf-8 -*-
from django.db import models

KEY_LENGTH=50

class Keyword(models.Model):
    value = models.CharField(max_length=100, primary_key=True) 

    def __unicode__(self):
        return self.value

class Profile(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)
    email = models.EmailField(max_length=75)
    keywords = models.ManyToManyField(Keyword)
    key = models.CharField(max_length=KEY_LENGTH)
    
    def summary(self):
        result = ''
        for k in self.keywords.all():
            result += k.value+', '
        if len(result) > 0:
            result=result[:-2]
        return result

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)

class Invitation(models.Model):
    email = models.EmailField(max_length=50)
    key = models.CharField(max_length=KEY_LENGTH)

    def __unicode__(self):
        return self.email

class Comment(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=75)
    content = models.CharField(max_length=1024)
    key = models.CharField(max_length=KEY_LENGTH)

    def __unicode__(self):
        return self.name