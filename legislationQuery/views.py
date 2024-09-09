from django.shortcuts import render
from django.http import HttpResponse
from .models import LegislationQuery

# Create your views here.

def index(request):
    context = {
        'model' : LegislationQuery,
        'title' : 'Find Relevant Legislation | Legislation Assist',
    }
    return render(request, "legislationQuery/index.html", context)

def documentation(request):
    context = {
        'model': LegislationQuery,
        'title': 'Internal Documentation | Legislation Assist',
    }
    return render(request, "legislationQuery/documentation.html", context)