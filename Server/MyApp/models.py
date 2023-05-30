from django.db import models


class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    avatar = models.CharField(max_length=100)
    bio = models.TextField()
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Follow(models.Model):
    follower = models.CharField(max_length=30)
    followee = models.CharField(max_length=30)


class Block(models.Model):
    blocker = models.CharField(max_length=30)
    blocked = models.CharField(max_length=30)


class Message(models.Model):
    sender = models.CharField(max_length=30)
    receiver = models.CharField(max_length=30)
    content = models.TextField()
    c_time = models.DateTimeField(auto_now_add=True)


class Session(models.Model):
    username = models.CharField(max_length=30)
    target = models.CharField(max_length=30)
    last_message = models.TextField()
    message_cnt = models.IntegerField(default=0)
    message_not_checked = models.IntegerField(default=0)
    c_time = models.DateTimeField(auto_now_add=True)


class Moment(models.Model):
    username = models.CharField(max_length=30)
    avatar = models.CharField(max_length=100)
    type = models.CharField(max_length=10, default='未分类')
    content = models.TextField(default=' ')
    media = models.CharField(max_length=100, default='null')
    location = models.CharField(max_length=100, default='null')
    likes_count = models.IntegerField(default=0)
    favorites_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    c_time = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    username = models.CharField(max_length=30)
    moment_id = models.IntegerField()


class Favorite(models.Model):
    username = models.CharField(max_length=30)
    moment_id = models.IntegerField()


class Comment(models.Model):
    username = models.CharField(max_length=30)
    moment_id = models.IntegerField()
    content = models.TextField()
    c_time = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    username = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    content = models.TextField()
    c_time = models.DateTimeField(auto_now_add=True)



