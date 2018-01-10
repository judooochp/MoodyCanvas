from django.shortcuts import render, get_object_or_404
from django.db import models
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.urls import reverse, path
from django.conf.urls import url
from django.template import loader
 
def index(request):
    template = 'home/index.html'
    return HttpResponse(template.render(None, request))