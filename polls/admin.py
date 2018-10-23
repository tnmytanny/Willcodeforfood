from django.contrib import admin

from .models import Question
from .models import Choice
from .models import Students

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Students)