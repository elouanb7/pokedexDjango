from django.shortcuts import render
import requests


def home(request):
    context = {'test': "test"}
    return render(request, template_name='index.html', context=context)
