from django.contrib import admin
from .models import Module,GroupPermission,Role

# Register your models here.
admin.site.register(Module)
admin.site.register(GroupPermission)
admin.site.register(Role)