from django.shortcuts import render, get_object_or_404
# get_object_or_404 >> 페이지 없음(404)
from .models import Question, Choice
from django.http import HttpResponse

# http 화면을 구성하는 기능 호출

# Create your views here.
def index(request):
    # return HttpResponse("Hello") 기존코드
	
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}


    return render(request, "polls/index.html", context)

def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

def vote(request, question_id):
    return HttpResponse(f"You're voting on question {question_id}.")

# <p Hello, world. You're at the pools index. /p> 처럼 코딩된 문장도 넣을 수 있음.
# ulrs 받아서 앱을 호출했고 app이 view에서 index 함수를 호출 >> 화면에 뿌려지기 까지 상태까지.

