from django.contrib import admin
from .models import Question, Choice

admin.site.register(Question)
admin.site.register(Choice)
# 여기 추가해 줘야 비로소 화면에 출력된다.
# admin.site.register(Choice)
# Register your models here.

