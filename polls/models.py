from django.db import models
# Create your models here.
# ORM - 테이블 만드는 요소들은 넣어라.
# models를 상속받아서 테이블을 만드는데, 테이블은 Class로 선언.
# 함수 추가 등은 Migrations 필요 없음, 다만 필드 하나를 추가하면
# 꼭 Migrations를 진행 해 주어야 함.

class Question(models.Model):
    #필드명        = 필드의 속성
    question_text = models.CharField(max_length=200)
    #Str 데이터 타입(속성값 => max_length)
    pub_date = models.DateTimeField('date published')
    #날짜 데이터는 소숫점이 없으므로 int 값.
#테이블 형태로 예를 들어 이해해보자
#   Question이라는 테이블
#   -------------------------
#   |Question_text |pub_date|
#   -------------------------
#   |기타 등등...   |        |
#   -------------------------
    def __str__(self):
        return f"{self.id} | {self.question_text} | {self.pub_date}"
    # Object 객체를 한글로 변환.
    
    def was_published_recently(self):
        from django.utils import timezone
        import datetime
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1) and self.pub_date <= timezone.now()
        #Today = 2026.01.22.15:15 기준으로 24시간 내에 쓴 글이어야 함.
        #2026.01.22.09:15 >= 2026.01.21.15:15 >> 하루 내 만족 True 반환
        #2026.01.21.15:14 <= 2026.01.21.15:15 >> 하루 내 불만족
        #BUT 오늘 날짜보다 더 '미래'일 때
        # >> 2026.02.21.15:15 >= 2026.01.21.15:15 이것도 만족해 버리므로 이에대한
        # 예외처리 필요!!

    # 20시간 이내에 쓴건 True, 그외에는 False를 출력하도록.

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
