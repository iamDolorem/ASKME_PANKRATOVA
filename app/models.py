from django.db import models

# Create your models here.
# from django.db import models
# from django.contrib.auth.models import User
# from django.db.models import Count
#
#
# class ProfileManager(models.Manager):
#     def get_top_users(self, count=5):
#         return self.annotate(answer_count=Count('answer')).order_by('-answer_count')[:count]
#
#     def get_user_by_id(self, id):
#         try:
#             return self.annotate(question_count=Count('question', distinct=True),
#                                  answer_count=Count('answer', distinct=True)).get(id=id)
#         except Profile.DoesNotExist:
#             return None
#
#
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
#     avatar = models.ImageField(null=True, blank=True, upload_to='static/img/')
#     objects = ProfileManager()
#
#     def __str__(self):
#         return str(self.user.username)
#
#
# class TagManager(models.Manager):
#     def get_top_tags(self, count=7):
#         return self.annotate(q_count=Count('question')).order_by('-q_count')[:count]
#
#
# class Tag(models.Model):
#     name = models.CharField(max_length=20)
#     objects = TagManager()
#
#     def __str__(self):
#         return str(self.name)
#
#
# class QuestionManager(models.Manager):
#     def get_info_questions(self):
#         return self.annotate(count_answers=Count('answer', distinct=True),
#                              raiting=Count('likequestion', distinct=True) - Count('dislikequestion', distinct=True))
#
#     def get_new_questions(self):
#         return self.get_info_questions().order_by('-publish_date')
#
#     def get_top_questions(self):
#         return self.get_info_questions().order_by('-raiting')
#
#     def get_questions_by_tag(self, tag_name):
#         return self.get_info_questions().filter(tags__name=tag_name).order_by('-publish_date')
#
#     def get_question(self, id):
#         try:
#             return self.get_info_questions().get(id=id)
#         except Question.DoesNotExist:
#             return None
#
#     def get_question_by_user(self, user_id):
#         return self.get_info_questions().filter(user_id=user_id).order_by('-publish_date')
#
#
# class Question(models.Model):
#     user = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     title = models.CharField(max_length=80)
#     text = models.CharField(max_length=2000)
#     tags = models.ManyToManyField(Tag)
#     publish_date = models.DateTimeField(auto_now_add=True)
#     objects = QuestionManager()
#
#     def __str__(self):
#         return str(self.title)
#
#
# class AnswerManages(models.Manager):
#     def get_info_answers(self):
#         return self.annotate(raiting=Count('likeanswer', distinct=True) - Count('dislikeanswer', distinct=True))
#
#     def get_answers_for_question(self, id):
#         return self.get_info_answers().filter(question_id=id).order_by('-is_correct', '-publish_date')
#
#
# class Answer(models.Model):
#     user = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     text = models.CharField(max_length=1000)
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     is_correct = models.BooleanField(default=False)
#     publish_date = models.DateTimeField(auto_now_add=True)
#     objects = AnswerManages()
#
#     def __str__(self):
#         return f"{str(self.text)[:80]}..."
#
#
# class LikeQuestion(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     from_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
#
#
# class DislikeQuestion(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     from_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
#
#
# class LikeAnswer(models.Model):
#     answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
#     from_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
#
#
# class DislikeAnswer(models.Model):
#     answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
#     from_user = models.ForeignKey(Profile, on_delete=models.CASCADE)

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils.timezone import now

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    avatar = models.ImageField(upload_to="static/img", null=True, blank=True)
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