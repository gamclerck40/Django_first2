from django.contrib import admin
from .models import Question, Choice

#아래 두 class들은 '선언' 만으로 동작함. 별도의 CSS, HTML, views.py 연결이 필요 없음.
# Choice 인라인 (Tabular 형식)
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

# Question 모델 커스터마이징
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("제목", {"fields": ["question_text"]}),
        ("날짜정보", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    # 우측에 
    search_fields = ["question_text"]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
# 여기 추가해 줘야 비로소 화면에 출력된다.
# admin.site.register(Choice)
# Register your models here.

