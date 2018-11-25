from django.contrib import admin

from .models import Question
from .models import Choice
from .models import Students
from .models import Instructors
from .models import AllProjects
from .models import UpdatedProject
from .models import Message
from .models import Chats
from .models import Document

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Students)
admin.site.register(Instructors)
admin.site.register(AllProjects)
admin.site.register(UpdatedProject)
admin.site.register(Message)
admin.site.register(Chats)
admin.site.register(Document)