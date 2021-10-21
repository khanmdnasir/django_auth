from django.contrib import admin

# Register your models here.


from users.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin


admin.site.register(User)
admin.site.unregister(Group)