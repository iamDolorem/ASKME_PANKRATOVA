from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils.timezone import now

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class QuestionManager(models.Manager):
    def best(self):
        return self.annotate(like_count=models.Count('liked_by')).order_by('-like_count')

    def newest(self):
        return self.order_by('-created_at')
        # return self.order_by('-created_at').distinct()

    def questions_by_tag(self, tag_name):
        return self.filter(tags__name=tag_name).order_by('-created_at')


class Question(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    objects = QuestionManager()

    # def likes_count(self):
    #     return self.questionlike_set.count()

    # def likes_count(self):
    #     return self.liked_by.count()

    def likes_count(self):
        return self.liked_by.count()

    def answers_count(self):
        return self.answers.count()

    objects = QuestionManager()

    def __str__(self):
        return self.title

class AnswerManager(models.Manager):
    def for_question(self, question):
        return self.filter(question=question).order_by('-created_at')

class Answer(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE,related_name='answers')
    is_correct = models.BooleanField(default=False)

    def likes_count(self):
        return self.liked_by.count()

    objects = AnswerManager()

    def __str__(self):
        return f"Answer by {self.author.username} on {self.question.title}"


class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='liked_by')

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return f"{self.user.username} liked {self.question.title}"


class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='liked_by')

    class Meta:
        unique_together = ('user', 'answer')

    def __str__(self):
        return f"{self.user.username} liked an answer on {self.answer.question.title}"