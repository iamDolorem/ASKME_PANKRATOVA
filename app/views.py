import copy

from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, get_object_or_404

from app.models import Question, Answer, Tag
from app.pagination import paginate_queryset

QUESTIONS = [
    {
        'title': F'Title {i}',
        'id': i,
        'text': f'This is text for question = {i}'
    } for i in range(30)
]

def index(request):
    questions = Question.objects.newest()
    per_page = 10
    page = paginate_queryset(request, questions, per_page)
    return render(request, "index.html", {
        'questions': page.object_list,
        'page_obj': page
    })


def hot(request):
    # hot_questions = copy.deepcopy(QUESTIONS)
    # hot_questions.reverse()  # Переворачиваем список "горячих" вопросов
    # page_num = int(request.GET.get('page', 1))  # Получаем номер страницы из запроса
    # paginator = Paginator(hot_questions, 5)  # Пагинируем перевернутый список
    # page = paginator.page(page_num)  # Получаем текущую страницу
    # return render(
    #     request, 'hot.html',
    #     context={'questions': page.object_list, 'page_obj': page}  # Передаем пагинированный список
    # )
    questions = Question.objects.best()
    per_page = 5
    page = paginate_queryset(request, questions, per_page)
    return render(request, "hot.html", {
        'questions': page.object_list,
        'page_obj': page
    })

def question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    # one_question = QUESTIONS[question_id]
    # related_questions = QUESTIONS.values()  # Предположим, это список всех вопросов
    # return render(
    #     request, 'one_question.html',
    #     {'item': one_question, 'questions': related_questions}  # Передаём и `questions`
    # )
    answers = Answer.objects.for_question(question)

    per_page = 5
    page = paginate_queryset(request, answers, per_page)

    return render(request, "one_question.html", {
        'question': question,
        'answers': page.object_list,
        'page_obj': page,
    })


def setting(request):
    return render(
        request, 'settings.html',
    )

def askform(request):
    return render(
        request, 'ask.html',
    )

def maincard(request):
    return render(
        request, 'question.html',
    )

def card(request):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(QUESTIONS, 5)
    page = paginator.page(page_num)
    return render(
        request, 'question.html',
        context={'questions': page.object_list, 'page_obj': page}
    )

def youranswer(request):
    return render(
        request, 'question.html',
    )

def tag_questions(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)  # Получаем тег или 404, если не найден
    tag_questions = Question.objects.questions_by_tag(tag_name)

    per_page = 5
    page = paginate_queryset(request, tag_questions, per_page)
    return render(request, "tag.html", {
        'tag': tag,
        'questions': page.object_list,
        'page_obj': page
    })