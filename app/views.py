import copy

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

QUESTIONS = [
    {
        'title': F'Title {i}',
        'id': i,
        'text': f'This is text for question = {i}'
    } for i in range(30)
]


def index(request):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(QUESTIONS, 5)
    page = paginator.page(page_num)
    return render(
        request, 'index.html',
        context={'questions': page.object_list, 'page_obj': page}
    )

def hot(request):
    hot_questions = copy.deepcopy(QUESTIONS)
    hot_questions.reverse()
    return render(
        request, 'hot.html',
        context={'questions': hot_questions}
    )

def question(request, question_id):
    one_question = QUESTIONS[question_id]
    return render(
        request, 'one_question.html',
        {'item': one_question}
    )

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