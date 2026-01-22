from django.urls import path 
from . import views

app_name = "polls"
#App 이름을 선언해줘야 화면이 제대로 뜬다! 이번 버전부터 더 엄격해진듯.

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    # http://127.0.0.1:8000/polls/
    # views.index는 <a href="{% url 'index' %}">홈으로</a> 기능인 함수 
    # (도메인주소, views.py의 함수 호출,탬플릿 이름(html에서 호출될 이름))
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),

]
