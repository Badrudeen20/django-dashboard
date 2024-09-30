from django.db import models


class Posts(models.Model):
    name = models.TextField()
    image = models.TextField()
    rate = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    lang = models.TextField()
    genre = models.TextField()
    story = models.TextField()
    link = models.CharField(max_length=100)
    more = models.TextField()
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Trand(models.Model):
    post = models.ForeignKey(Posts,related_name="posts", on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Menu(models.Model):
    name = models.CharField(max_length=100)
    menuId = models.CharField(max_length=100,null=True)
    status = models.CharField(max_length=100)
    



