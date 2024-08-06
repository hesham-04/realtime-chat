from django.contrib import admin

from a_rtchat import models

# Register your models here.
admin.site.register(models.GroupMessage)
admin.site.register(models.ChatGroup)
