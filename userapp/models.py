from django.db import models

# Create your models here.
class Questionairre(models.Model):
    username = models.CharField(max_length=1000)
    answerone = models.TextField()
    answertwo = models.TextField()
    answerthree = models.TextField()
    answerfour = models.TextField()
    answerfive = models.TextField()
    answersix = models.TextField()