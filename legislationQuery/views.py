from django.shortcuts import render
from django.template.loader import render_to_string
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
        user_query = parsed_json.get('userQuery')
        print("user's query:", user_query)

        # Using async in order not to have to poll/auto refresh, and instead receive a real time response. 
        client = AsyncOpenAI(
        api_key=os.environ.get('OPEN_API_KEY'),
        # Sets custom timeout settings via open ai's httpx client. E.g. will wait 6 seconds for a read response, 10 for a write response.
        timeout=httpx.Timeout(70.0),
        )

      
        async def main():
            chat_completion = await client.chat.completions.create(
            messages=[
                {'role': 'user', 'content': user_query},
                {'role': 'system', 'content': '''You are a lawyer writing a research memo. Provide a list of legislation (i.e. statutes, regulations and by-laws) relevant to the legal issue the user has asked about. Include a lot of legislation, be very inclusive. Format 
                 it by title of the legislation, and a detailed summary of what the legislation is about, and a detailed explanation of why it might apply to the legal issue.'''},
                 {'role': 'system', 'content': '''Do not answer any questions that aren't related to providing legislation. If such a question is asked, just reply with "Unfortunately, Legislation Assist is limited
                  to the provision of references to legislation for legal issues. It is unable to provide answers to other queries."'''},
            ],
            model='gpt-4o-2024-08-06',
            temperature=1,

            )

            return chat_completion
        
        answer_from_gpt = asyncio.run(main())

        answer_processed = answer_from_gpt.choices[0].message.content

  
        print(answer_processed)


        context = {
            'user_query': user_query,
            'answer_from_gpt': answer_processed,
        }

        html_insert = render_to_string('legislationQuery/partials/queries-and-answers.html', context)

        return HttpResponse(html_insert)