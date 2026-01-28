from django.shortcuts import render, get_object_or_404
# get_object_or_404 >> 페이지 없음(404)
from .models import Question, Choice
from django.db.models import F
from django.urls import reverse
from django.views import generic
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse_lazy


# http 화면을 구성하는 기능 호출
# render의 구조 (request: 템플릿에서 request.user, request.path 같은 값에 접근,
#               template_name: 렌더링할 템플릿 파일 경로, context: 템플릿에 전달할 데이터 딕셔너리, 
#               content_type: HTTP 응답의 Content-Type|기본값은 text/html, status: HTTP 상태 코드[ex:200, 403, 404, 500]
#               using: 사용할 템플릿 엔진 지정|여러 템플릿 엔진을 사용할 때 필요)
#               >> *뷰(View)*에서 템플릿을 HTML로 렌더링해서 HttpResponse 객체로 반환해주는 헬퍼 함수

# HttpResponse의 구조 (content: 클라이언트에게 보낼 본문 내용|str → 자동으로 bytes로 변환|bytes도 가능 -> ex)"String텍스트")
#                     

# FBV(Function-Based View 구현)
# def index(request):
#     # return HttpResponse("Hello") 기존코드
	
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     context = {"latest_question_list": latest_question_list}

#     return render(request, "polls/index.html", context)
#     #결론은 'render'를 통해 최종적으로 화면에 뿌려주는 역할.

# def detail(request, question_id):
#      question = get_object_or_404(Question, pk=question_id)
#      #고유 번호와, Question 모델을 같이 받아 -> 해당 id정보가 존재하지 않으면 404 에러를 반환
#      context = {"question": question}
#      return render(request, "polls/detail.html", context)

# #'detail'함수의 try-except 버전.
# # def detail(request, question_id):
# #     try:
# #         question = Question.objects.get(pk=question_id)
# #     except Question.DoesNotExist:
# #         raise Http404("Question does not exist")
# #     return render(request, "polls/detail.html", {"question": question})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     context = {"question": question}
#     return render(request, "polls/results.html", context)

# def vote(request, question_id):
#     return HttpResponse(f"You're voting on question {question_id}.")

# def aa(request):
#     questions = Question.objects.all()
#     choices = Question.objects.all()
#     return render(request, "polls/aa.html", {"questions": questions,
#                                              "choices": choices})

# # <p Hello, world. You're at the pools index. /p> 처럼 코딩된 문장도 넣을 수 있음.
# # ulrs 받아서 앱을 호출했고 app이 view에서 index 함수를 호출 >> 화면에 뿌려지기 까지 상태까지.

#CBV (Class-Based View)
class IndexView(generic.ListView):
    model = Question
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
# 질문 상세 페이지
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    context_object_name = "question"
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())    
    
# 결과 페이지 (DetailView 클래스 활용 - html 구현하기 나름.)
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
    context_object_name = "question"
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

# 투표 처리 로직
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"]) #request.POST["choice"] -> 선택한 Choice의 PK값을 요청값으로 반환.
        # 투표 페이지에서 아무것도 선택하지 않고 '투표' 버튼을 누르면 생기는 에러 예외처리.
    except (KeyError, Choice.DoesNotExist):
    # KeyError -> Choice 선택 안했을 때 키값을 못받아와서 생긴 오류
    # Choice.DoesNotExist -> Choice가 애초에 하나도 없을 때.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message":"You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        # 어제 강의 참고.. 상세 설명 하셨음.
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
class QuestionCreateView(generic.CreateView):
    model = Question
    fields = ["question_text", "pub_date"]
    template_name = "polls/question_form.html"
    success_url = reverse_lazy("polls:index")

class QuestionUpdateView(generic.UpdateView):
    model = Question
    fields = ["question_text", "pub_date"]
    template_name = "polls/question_form.html"
    success_url = reverse_lazy("polls:index")

class QuestionDeleteView(generic.DeleteView):
    model = Question
    template_name = "polls/question_confirm_delete.html"
    success_url = reverse_lazy("polls:index")