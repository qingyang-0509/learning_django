import datetime

from django.db import models
from django.utils import timezone
'''
Each model is represented by a class that subclasses django.db.models.Model. 
Each model has a number of class variables, each of which represents a database feld in the model.
Each feld is represented by an instance of a Field class - e.g., CharField for character felds and DateTimeField for datetimes. 
'''


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    # # Question.was_published_recently() should return False if its pub_date is in the future.
    # def was_published_recently(self):
    #     return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
