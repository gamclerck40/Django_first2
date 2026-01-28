# 쿼리스트링용: 날짜 파싱
import datetime


def _parse_yyyy_mm_dd(value: str):
    # 🔹 _parse_yyyy_mm_dd
    # - 이 이름은 파이썬에 이미 존재하는 게 아님
    # - 전부 개발자가 지은 "함수 이름"
    # - 앞의 '_' (언더스코어 1개)는 파이썬 문법 ❌, 개발자 관례 ⭕
    #   → "이 함수는 내부에서만 쓰는 헬퍼 함수입니다" 라는 의미
    #
    # 🔹 함수(function) vs 메서드(method)
    # - 이 함수는 클래스 밖에 정의됨 → 함수(function)
    # - 메서드(method)는 반드시 class 안에 정의됨

    """
    'YYYY-MM-DD' 형식 문자열을 date로 파싱.
    실패하면 None 반환.
    """

    try:
        # 🔹 datetime.date.fromisoformat
        # - fromisoformat 은 파이썬 표준 라이브러리(datetime)에 이미 정의된 메서드
        # - 개발자가 만든 함수 ❌
        # - date 클래스에 소속된 메서드 ⭕
        #
        # 🔹 isoformat 이란?
        # - ISO 8601 국제 표준 날짜 형식
        # - 예: '2026-01-27'
        #
        # 🔹 즉 이 줄의 의미는:
        # "YYYY-MM-DD 문자열을 date 객체로 변환하라"
        return datetime.date.fromisoformat(value)

    except (TypeError, ValueError):
        # 🔹 TypeError
        # - value가 None 같은 타입 자체가 잘못된 경우
        #
        # 🔹 ValueError
        # - 문자열이지만 날짜 형식이 잘못된 경우
        #   예: '2026-13-40', 'abc'
        #
        # 🔹 실패 시 None을 반환하는 이유
        # - 뷰 로직에서 "if start:" 같은 조건문으로
        #   안전하게 필터 적용 여부를 판단하기 위함
        return None


# 쿼리스트링 처리: IndexView(get_queryset)
class IndexView(generic.ListView):
    # 🔹 IndexView
    # - Django의 ListView를 상속받은 클래스
    # - 이 안에 정의된 함수들은 "메서드(method)"

    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        # 🔹 get_queryset
        # - Django ListView에 이미 정의된 메서드를 "오버라이드"한 것
        # - 이 이름은 개발자가 마음대로 바꾸면 ❌
        # - Django가 내부적으로 호출하는 약속된 메서드

        qs = Question.objects.all()
        # 🔹 qs
        # - QuerySet의 약자
        # - Question 테이블 전체를 의미하는 객체

        # 1) show=future → 미래 질문 포함 여부 (기본: 미래 숨김)
        show = self.request.GET.get("show")
        # 🔹 self.request.GET
        # - request 객체는 Django가 자동으로 넣어줌
        # - GET은 쿼리스트링 딕셔너리

        if show != "future":
            # 🔹 pub_date__lte
            # - __lte 는 Django ORM 문법
            # - "less than or equal" (이하)
            qs = qs.filter(pub_date__lte=timezone.now())

        # 2) q=키워드 → question_text 검색
        q = (self.request.GET.get("q") or "").strip()
        # 🔹 strip()
        # - 문자열 메서드 (파이썬 내장)
        # - 양쪽 공백 제거

        if q:
            # 🔹 question_text__icontains
            # - __icontains : 대소문자 구분 없는 포함 검색
            qs = qs.filter(question_text__icontains=q)

        # 3) start/end=YYYY-MM-DD → 기간 필터
        start = _parse_yyyy_mm_dd(self.request.GET.get("start"))
        end = _parse_yyyy_mm_dd(self.request.GET.get("end"))
        # 🔹 여기서 _parse_yyyy_mm_dd 호출
        # - 내부용 헬퍼 함수 재사용
        # - 파싱 실패 시 None 반환 → 아래 if 문에서 자동으로 걸러짐

        if start:
            # 🔹 pub_date__date__gte
            # - __date : DateTime → Date 부분만 비교
            # - __gte  : greater than or equal (이상)
            qs = qs.filter(pub_date__date__gte=start)

        if end:
            qs = qs.filter(pub_date__date__lte=end)

        # 4) order=oldest → 정렬 (기본: 최신순)
        order = self.request.GET.get("order")

        if order == "oldest":
            qs = qs.order_by("pub_date")
        else:
            qs = qs.order_by("-pub_date")
            # 🔹 '-' 붙으면 내림차순 (최신순)

        # 5) (옵션) 목록 5개 제한 유지
        return qs[:5]
        # 🔹 슬라이싱
        # - QuerySet에서도 파이썬 슬라이싱 문법 사용 가능