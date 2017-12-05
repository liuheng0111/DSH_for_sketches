# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Image(models.Model):
    path = models.CharField(max_length=200)
    code = models.CharField(max_length=50)