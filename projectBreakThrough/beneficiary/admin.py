from django.contrib import admin
from .models import Appeal , Message , Profile

# Register your models here.

admin.site.register(Appeal ),

admin.site.register(Message),

admin.site.register(Profile)
