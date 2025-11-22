from django.http import HttpResponse
from django.shortcuts import render

from .models import Sample

def index(request):
    return HttpResponse("Hello world. You're at the application index")

def samples_list(request):
    samples = Sample.objects.all()
    return render(request, "samples.html", {"samples": samples})