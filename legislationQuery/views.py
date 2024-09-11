from django.shortcuts import render
from django.http import HttpResponse
from .models import LegislationQuery
import os
import httpx
import asyncio
import json
from openai import AsyncOpenAI
from django.conf import settings
from dotenv import load_dotenv


# Create your views here.

# Path to environment variable file
load_dotenv(dotenv_path=os.path.join(settings.BASE_DIR, '.env'))

def index(request):

    context = {
        'legislation_queries_answers' : LegislationQuery.objects.all(),
        'title' : 'Find Relevant Legislation | Legislation Assist',
    }
    return render(request, 'legislationQuery/index.html', context)

def documentation(request):
    context = {
        'legislation_queries_answers': LegislationQuery.objects.all(),
        'title': 'Internal Documentation | Legislation Assist',
    }
    return render(request, 'legislationQuery/documentation.html', context)


def open_ai_connect(request):

    if (request.method) == 'POST':
        parsed_json = json.loads(request.body)
        userQuery = parsed_json.get('userQuery')
        print(userQuery)

        # Using async in order not to have to poll/auto refresh, and instead receive a real time response. 
        client = AsyncOpenAI(
        api_key=os.environ.get('OPEN_API_KEY'),
        # Sets custom timeout settings via open ai's httpx client. E.g. will wait 6 seconds for a read response, 10 for a write response.
        timeout=httpx.Timeout(120.0, read=6.0, write=10.0, connect=4.0),
        )

        # user_query = request.
        # should remove "None"? given U WILL BE PRINTING OUT TO TEMPLATE?
        async def main() -> None:
            chat_completion = await client.chat.completions.create(
            messages=[
                {'role': 'user', 'content': userQuery},
                {'role': 'system', 'content': 'Answer in a consistent style.'},
            ],
            model='gpt-4o-2024-08-06',
            temperature=0,

            )

        return render()