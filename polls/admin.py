from django.contrib import admin

from .models import Students
from .models import Instructors
from .models import AllProjects
from .models import AppliedProject
from .models import Message
from .models import Chats
from .models import Document

admin.site.register(Students)
admin.site.register(Instructors)
admin.site.register(AllProjects)
admin.site.register(AppliedProject)
admin.site.register(Message)
admin.site.register(Chats)
admin.site.register(Document)