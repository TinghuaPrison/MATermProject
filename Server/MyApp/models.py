from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    avatar = models.CharField(max_length=100)
    bio = models.TextField()
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Follow(models.Model):
    follower_id = models.IntegerField()
    followee_id = models.IntegerField()


class Post(models.Model):
    user_id = models.IntegerField()
    username = models.CharField(max_length=30)
    type = models.CharField(max_length=10)
    content = models.TextField()
    location = models.CharField(max_length=100)
    likes_count = models.IntegerField()
    comments_count = models.IntegerField()
    favorites_count = models.IntegerField()
    c_time = models.DateTimeField(auto_now_add=True)


class Likes(models.Model):
    user_id = models.IntegerField()
    post_id = models.IntegerField()


class Comments(models.Model):
    user_id = models.IntegerField()
    post_id = models.IntegerField()
    content = models.TextField()
    c_time = models.DateTimeField(auto_now_add=True)


class Favorites(models.Model):
    user_id = models.IntegerField()
    post_id = models.IntegerField()


class Block(models.Model):
    blocker_id = models.IntegerField()
    blocked_id = models.IntegerField()


class Message(models.Model):
    sender_id = models.IntegerField()
    receiver_id = models.IntegerField()
    content = models.TextField()
    c_time = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    user_id = models.IntegerField()
    type = models.CharField(max_length=10)
    content = models.TextField()
    c_time = models.DateTimeField(auto_now_add=True)



