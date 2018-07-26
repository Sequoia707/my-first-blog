from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Question
from django.urls import reverse

# Create your tests here.

class QuestionModelTests(TestCase):
	
	def test_was_published_recently_with_future_question(self):
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertIs(future_question.was_published_recently(), False)

	def test_was_publisehd_recently_with_old_question(self):
		time = timezone.now() - datetime.timedelta(days=1, seconds=1)
		old_question = Question(pub_date=time)
		self.assertIs(old_question.was_published_recently(), False)

	def test_was_published_recently_with_recent_question(self):
		time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
		recent_question = Question(pub_date=time)
		self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):

	def test_no_questions(self):
		response = self.client.get(reverse('webapp:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls available, man")
		self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_past_question(self):
		create_question(question_text="Past question", days=-30)
		response = self.client.get(reverse('webapp:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question>'])

	def test_future_question(self):
		create_question(question_text="Futue question", days=30)
		response = self.client.get(reverse('webapp:index'))
		self.assertContains(response, "No polls available, man")
		self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_future_question_and_past_question(self):
		create_question(question_text="Past question", days=-30)
		create_question(question_text="Future question", days=30)
		response = self.client.get(reverse('webapp:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question>'])
		
	def test_two_past_question(self):
		create_question(question_text="Past question one", days=-30)
		create_question(question_text="Past question two", days=-5)
		response = self.client.get(reverse('webapp:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question two>', '<Question: Past question one>'])

class QuestionDetailViewTests(TestCase):
	def test_future_question(self):
		future_question = create_question(question_text="Future question", days=5)
		url = reverse('webapp:detail', args=(future_question.id,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)
	
	def test_past_question(self):
		past_question = create_question(question_text="Past question", days=-5)
		url = reverse('webapp:detail', args=(past_question.id,))
		response = self.client.get(url)
		self.assertContains(response, past_question.question_text)

class QuestionResultsViewTests(TestCase):

	def test_future_question(self):
		future_question = create_question(question_text="Future question", days=5)
		url = reverse('webapp:results', args=(future_question.id,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)
	
	def test_past_question(self):
		past_question = create_question(question_text="Past question", days=-5)
		url = reverse('webapp:results', args=(past_question.id,))
		response = self.client.get(url)
		self.assertContains(response, past_question.question_text)







