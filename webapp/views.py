from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone


# Create your views here.

class IndexView(generic.ListView):
	template_name = 'webapp/index.html'
	context_object_name = 'latest_question_list'
	
	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Question
	template_name = 'webapp/detail.html'
	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'webapp/results.html'
	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'webapp/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice!",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('webapp:results', args=(question.id,)))


		


