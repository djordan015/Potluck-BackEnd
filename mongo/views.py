from django.http import HttpResponse
from django.shortcuts import render

from .models import Sample

def index(request):
    return HttpResponse("Hello world. You're at the application index")

def samples_list(request):
    # Query the Sample model (note: model is named `Sample`)
    samples = Sample.objects.all()
    # render(template takes request as first arg)
    return render(request, "samples.html", {"samples": samples})