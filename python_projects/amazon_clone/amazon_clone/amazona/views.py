from django.shortcuts import render, redirect
from time import gmtime, strftime


def index(request):

    return render(request, 'index.html')
