from django.shortcuts import render

from django.http import HttpResponse


def home(request):
    return render(request, 'home.html', {'name': 'test'})
# Create your views here.
# This is new line


def add(request):
    val1 = int(request.POST['num1'])
    val2 = int(request.POST['num2'])
    sum = val1+val2
    return render(request, 'result.html', {'result': sum})
