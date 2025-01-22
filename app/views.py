from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.urls import reverse
from app.forms import AnswerForm, LoginForm, SignUpForm, ProfileEditForm, QuestionForm
from app.models import Question, Answer, Tag
from app.pagination import paginate_queryset
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import SignUpForm
from .models import Profile

QUESTIONS = [
    {
        'title': F'Title {i}',
        'id': i,
        'text': f'This is text for question = {i}'
    } for i in range(30)
]


def index(request):
    questions = Question.objects.newest()
    per_page = 5
    page = paginate_queryset(request, questions, per_page)
    return render(request, "index.html", {
        'questions': page.object_list,
        'page_obj': page
    })


def hot(request):
    questions = Question.objects.best()
    per_page = 5
    page = paginate_queryset(request, questions, per_page)
    return render(request, "hot.html", {
        'questions': page.object_list,
        'page_obj': page
    })


def question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.for_question(question)

    form = AnswerForm()

    per_page = 5
    page = paginate_queryset(request, answers, per_page)

    return render(request, "one_question.html", {
        'question': question,
        'answers': page.object_list,
        'page_obj': page,
        'form': form,
    })


def login_view(request):
    redirect_url = request.GET.get('continue', reverse('app:index'))

    if request.user.is_authenticated:
        return redirect(redirect_url)

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect(redirect_url)
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form, 'continue': redirect_url})


def logout_view(request):
    logout(request)
    next_url = request.GET.get('next', '/')
    print(f"Redirecting to: {next_url}")
    return redirect(next_url)


def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"]
            )

            profile = Profile.objects.create(user=user)

            avatar = form.cleaned_data.get("avatar")
            if avatar:
                profile.avatar = avatar
                profile.save()

            login(request, user)
            return redirect("app:index")

    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})



@login_required
def setting(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()

            avatar = request.FILES.get('avatar')
            if avatar:
                user.profile.avatar = avatar
                user.profile.save()

            return redirect('app:settings')
    else:
        form = ProfileEditForm(instance=user)

    return render(request, 'settings.html', {'form': form, 'user': user})


@login_required
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user.profile
            form.save(commit=True)
            form.save(commit=True)
            return redirect('app:one_question', question_id=question.id)
    else:
        form = QuestionForm()

    return render(request, 'ask.html', {'form': form})


@login_required
def add_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user.profile
            answer.question = question
            answer.save()
            return redirect(f'/question/{question_id}#answer-{answer.id}')
    else:
        form = AnswerForm()

    return redirect('app:question_detail', question_id=question_id)

def tag_questions(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    tag_questions = Question.objects.questions_by_tag(tag_name)

    per_page = 5
    page = paginate_queryset(request, tag_questions, per_page)
    return render(request, "tag.html", {
        'tag': tag,
        'questions': page.object_list,
        'page_obj': page
    })