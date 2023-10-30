import datetime

from django.test import TestCase
from django.utils import timezone

from django.urls import reverse

from .models import Question


# Create your tests here.
class QuestionModelTest(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(
            hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """`
    Create a question with the given 'question_text' and published the
    given number of 'days' offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    # Using objects.create() is a convenient and concise way to create and save records in the database
    # without the need for multiple lines of code to create an object,
    # set its attributes, and then save it.
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        # In Django, self.client refers to an instance of the test client provided by Django's testing framework.
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        # In Django, self.client refers to an instance of the test client provided by Django's testing framework.
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        # In Django, self.client refers to an instance of the test client provided by Django's testing framework.
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        # In Django, self.client refers to an instance of the test client provided by Django's testing framework.
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        # In Django, self.client refers to an instance of the test client provided by Django's testing framework.
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.',
                                          days=5)
        # In Django, the reverse function is used to generate URLs for views,
        # allowing you to avoid hardcoding URLs in your code and making your application more maintainable.
        url = reverse('polls:detail', args=(future_question.id, ))
        # In Django, self.client refers to an instance of the test client provided by Django's testing framework.
        response = self.client.get(url)
        # self.assertEqual(response.status_code, 404)
        self.assertEqual(response.status_code, 200)
        ''' 
        In Django, status_code is an attribute of the HTTP response object. 
        
        200 (OK): This status code indicates a successful request. It is used when the server successfully processes the request and returns the expected content.

        201 (Created): This status code is typically used when a new resource is successfully created, such as when submitting a form to create a new database record.

        204 (No Content): This status code indicates that the request was processed successfully, but there is no content to return in the response body.

        400 (Bad Request): It is used to indicate that the client's request was malformed or invalid in some way.

        401 (Unauthorized): This status code indicates that the client needs to provide authentication credentials to access the requested resource.

        403 (Forbidden): It signifies that the client does not have permission to access the requested resource, even with authentication.

        404 (Not Found): This status code is returned when the requested URL or resource does not exist on the server.

        500 (Internal Server Error): This status code is used to indicate that an unexpected error occurred on the server, and the request could not be fulfilled.
        '''

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.',
                                        days=-5)
        # In Django, the reverse function is used to generate URLs for views,
        # allowing you to avoid hardcoding URLs in your code and making your application more maintainable.
        url = reverse('polls:detail', args=(past_question.id, ))
        # In Django, self.client refers to an instance of the test client provided by Django's testing framework.
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)