from django.contrib import admin

# Register your models here.
from . import models


admin.site.register(models.User)
admin.site.register(models.Block)
admin.site.register(models.Likes)
admin.site.register(models.Post)
admin.site.register(models.Notification)
admin.site.register(models.Message)
admin.site.register(models.Favorites)
admin.site.register(models.Comments)
admin.site.register(models.Follow)

