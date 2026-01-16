from django.apps import AppConfig

# Django가 모델의 기본 자동 필드(primary key)로 어떤 타입을 사용할지를 지정하기 위한 설정입니다.
class PollsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'

    # def ready(self):
    #     import polls.signals # 앱 시작 시 실행할 초기 설정

