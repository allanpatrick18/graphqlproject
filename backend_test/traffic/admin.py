from django.contrib import admin

from .models import User
from .models import Website
from .models import Visit
from .models import Stats
admin.site.register(User)
admin.site.register(Website)
admin.site.register(Visit)
admin.site.register(Stats)
# Register your models here.
