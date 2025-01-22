from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Question, Tag, Answer


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        label="Логин",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш логин'})
    )
    password = forms.CharField(
        required=True,
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким логином не найден.")
        return username

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        user = authenticate(username=username, password=password)

        if username and not user:
            raise forms.ValidationError("Неверный пароль.")

        self.user = user
        return password

class SignUpForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        label="Логин",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите логин"})
    )
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Введите email"})
    )
    password = forms.CharField(
        required=True,
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Введите пароль"})
    )
    password_repeat = forms.CharField(
        required=True,
        label="Повторите пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Повторите пароль"})
    )
    avatar = forms.ImageField(
        required=False,
        label="Загрузить аватар",
        widget=forms.FileInput(attrs={"class": "form-control"})
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Пользователь с таким логином уже существует.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже зарегистрирован.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_repeat = cleaned_data.get("password_repeat")

        if password and password_repeat and password != password_repeat:
            self.add_error("password_repeat", "Пароли не совпадают.")

        return cleaned_data


class ProfileEditForm(forms.ModelForm):
    avatar = forms.ImageField(
        required=False,
        label="Загрузить новый аватар",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email', 'username']
        labels = {
            'email': 'Email',
            'username': 'Логин',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }


class QuestionForm(forms.ModelForm):
    tags = forms.CharField(
        required=True,
        label="Теги",
        help_text="Введите теги через запятую, например: SQL, Python, C++",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']
        labels = {
            'title': 'Название',
            'text': 'Содержание',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 100}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
        if not tag_list:
            raise forms.ValidationError("Добавьте хотя бы один тег.")
        return tag_list

    def save(self, commit=True):
        question = super().save(commit=False)
        if commit:
            question.save()
            tags = self.cleaned_data['tags']
            tag_objects = []
            for tag_name in tags:
                tag_name = tag_name.strip()
                if  tag_name:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    tag_objects.append(tag)
            question.tags.set(tag_objects)
        return question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        labels = {
            'text': '',
        }
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Введите ваш ответ...'
            }),
        }

    def clean_content(self):
        text = self.cleaned_data.get('text', '').strip()
        if not text:
            raise forms.ValidationError("Ответ не может быть пустым.")
        return text