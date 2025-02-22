from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.template.context_processors import static
from django.urls import path
from django.conf.urls.static import static

from app import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('question/<int:question_id>', views.question, name='one_question'),
    path('question/<int:question_id>/add-answer/', views.add_answer, name='add_answer'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.register_view, name='signup'),
    path('settings/', views.setting, name='settings'),
    path('ask/', views.ask_question, name='ask'),
    path('admin/', admin.site.urls),
    path('tag/<str:tag_name>', views.tag_questions, name='tag'),
    path('like/', views.like_question, name='like_question'),
    path('like-answer/', views.like_answer, name='like_answer'),
    path('mark-answer-correct/', views.mark_answer_correct, name='mark_answer_correct'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)