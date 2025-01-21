import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike


class Command(BaseCommand):
    help = "Fill the database with test data."

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help="Multiplication ratio for test data.")

    def handle(self, *args, **options):
        ratio = options['ratio']

        self.stdout.write(f"Creating {ratio} users...")
        users = []
        for i in range(ratio):
            username = f"user_{i + 1}"
            email = f"user_{i + 1}@example.com"
            user = User(username=username, email=email)
            user.set_password("password")
            users.append(user)
        User.objects.bulk_create(users)
        self.stdout.write(f"Created {ratio} users.")

        users = list(User.objects.all())

        self.stdout.write("Creating profiles for users...")
        profiles = [Profile(user=user) for user in users]
        Profile.objects.bulk_create(profiles, ignore_conflicts=True)

        self.stdout.write(f"Creating {ratio} tags...")
        tags = []
        for i in range(ratio):
            tag_name = f"tag_{i + 1}"
            tags.append(Tag(name=tag_name))
        Tag.objects.bulk_create(tags)
        self.stdout.write(f"Created {ratio} tags.")

        tags = list(Tag.objects.all())

        # profiles = list(Profile.objects.all())  # Используем Profile вместо User

        self.stdout.write(f"Creating {ratio * 10} questions...")
        questions = []
        for i in range(ratio * 10):
            question = Question(
                title=f"Question title {i + 1}",
                text=f"Question content {i + 1}",  # Замените content на question
                author=random.choice(profiles),  # Здесь выбираем Profile
            )
            questions.append(question)
        Question.objects.bulk_create(questions)
        self.stdout.write(f"Created {ratio * 10} questions.")

        questions = list(Question.objects.all())

        self.stdout.write("Assigning tags to questions...")
        for question in questions:
            question.tags.set(random.sample(tags, k=min(3, len(tags))))

        self.stdout.write(f"Creating {ratio * 100} answers...")
        answers = []
        for i in range(ratio * 100):
            answer = Answer(
                text=f"Answer content {i + 1}",
                author=random.choice(profiles),
                question=random.choice(questions),
            )
            answers.append(answer)
        Answer.objects.bulk_create(answers)
        self.stdout.write(f"Created {ratio * 100} answers.")

        answers = list(Answer.objects.all())

        self.stdout.write("Creating unique likes for questions...")
        self.create_unique_likes(QuestionLike, users, questions, min(ratio * 200, len(users) * len(questions)))

        self.stdout.write("Creating unique likes for answers...")
        self.create_unique_likes(AnswerLike, users, answers, min(ratio * 200, len(users) * len(answers)))

        self.stdout.write(self.style.SUCCESS("Database filled successfully!"))


    def create_unique_likes(self, model, users, objects, likes_to_create):
        """
        Создает уникальные лайки для указанной модели.
        :param model: Модель лайков (QuestionLike или AnswerLike).
        :param users: Список пользователей.
        :param objects: Список объектов (вопросов или ответов).
        :param likes_to_create: Количество лайков для создания.
        """
        existing_likes = set()  # Множество для отслеживания уникальных пар (user_id, object_id)
        likes = []
        while len(existing_likes) < likes_to_create:
            user = random.choice(users)
            obj = random.choice(objects)
            pair = (user.id, obj.id)  # Пара (пользователь, объект)
            if pair not in existing_likes:
                existing_likes.add(pair)
                # Проверяем, для какой модели создается лайк
                if model == QuestionLike:
                    likes.append(model(user_id=user.id, question_id=obj.id))
                elif model == AnswerLike:
                    likes.append(model(user_id=user.id, answer_id=obj.id))
            # Пакетная вставка для снижения нагрузки
            if len(likes) >= 10000:
                model.objects.bulk_create(likes)
                likes = []
        # Вставляем оставшиеся лайки
        if likes:
            model.objects.bulk_create(likes)