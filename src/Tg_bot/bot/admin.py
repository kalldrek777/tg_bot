from django.contrib import admin
from bot.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['external_id']

admin.site.register(User, UserAdmin)


