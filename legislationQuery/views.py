from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from .models import LegislationQuery
from django.utils.safestring import mark_safe
import os
import markdown
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

        # Insert rate limiter here.
        #temporary somewhat pseudo code below:
        if LegislationQuery.objects.all.most_recent().id == 20:
            if LegislationQuery.objects.all.mostrecent().id.created_date_time < currentdatetime(8am. this code is bad, it' just logic. checking if the id of the most recent instance was created the day before, and the current date time is the next day and it's past 8 am):
                LegislationQuery.objects.all.delete
                LegislationQuery.objects.all.create()
            else:
                sorry_message = "We apologize, but the daily limit for use of our app has been exceeded. Please return tomorrow after 8am once our usage limit resets."
                html_insert = render_to_string('legislationQuery/partials/queries-and-answers.html', {'sorry_message':sorry_message})
                return HttpResponse(html_insert)
        else:
            LegislationQuery.objects.all.create()


        
        parsed_json = json.loads(request.body)
        user_query = parsed_json.get('userQuery')
        # Backend check to prevent DB calls when user hasn't input a question. This is a redundancy in case an user disables specific JS code that prevents calls to backend.
        if user_query == ' ':
            html_insert = render_to_string('legislationQuery/partials/queries-and-answers.html', {'user_query':user_query,})
            return HttpResponse(html_insert)
      

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
                {'role': 'system', 'content': '''You are a lawyer writing a research memo. Only provide a list of legislation (i.e. statutes, regulations and by-laws) relevant to the legal issue. Include a lot of legislation. Format 
                 it by bolded name of the legislation, and a detailed summary section of what the legislation is about, and a detailed explanation section of why it might apply to the legal issue. Do not answer any questions that aren't related to providing legislation. Ask for a jurisdiction if one isn't provided. Your output should not use list tags.'''},
            ],
            model='gpt-4o-2024-08-06',
            temperature=0.8,

            )

            return chat_completion
        
        answer_from_gpt = asyncio.run(main())


        answer_processed = answer_from_gpt.choices[0].message.content

        print(answer_processed)

        html_answer_processed = markdown.markdown(answer_processed)

  
        print(html_answer_processed)

     
        html_insert = render_to_string('legislationQuery/partials/queries-and-answers.html', {'user_query':user_query, 'html_answer_processed':mark_safe(html_answer_processed),})

        return HttpResponse(html_insert)