from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse

from .models import Question

from django.template import loader

from django.http import Http404

# Create your views here.

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     output = ', '.join([q.question_text for q in latest_question_list])
#     return HttpResponse(output)

'''
It’s a very common idiom to load a template, 
fll a context and return an HttpResponse object with the result of therendered template. 
'''
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list' : latest_question_list,
    }
    return HttpResponse(template.render(context, request))
'''
It’s a very common idiom to load a template, 
fll a context and return an HttpResponse object with the result of therendered template. 
'''

'''
The render() function takes the request object as its frst argument, 
a template name as its second argument and a dictionary as its optional third argument. 
It returns an HttpResponse object of the given template rendered with the given context.
'''
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

# def detail(request, question_id):
#     return HttpResponse("You're looking at the question %s." % question_id)

# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, 'polls/detail.html', {'question': question})

'''
The get_object_or_404() function takes a Django model as its frst argument and an arbitrary number of keyword arguments, 
which it passes to the get() function of the model’s manager. It raises Http404 if the object doesn’t exist.
'''
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)