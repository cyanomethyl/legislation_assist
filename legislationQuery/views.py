from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from .models import LegislationQuery
from django.utils.safestring import mark_safe
from django.utils import timezone
import os
import markdown
import httpx
import asyncio
import bleach
import json
from openai import AsyncOpenAI
from django.conf import settings
from dotenv import load_dotenv



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

    if request.method == 'POST':
        # Resets instances of the LegislationQuery object to 0 instances, at 8am each day, only once per 24 hour period.
        reset_time_8am = timezone.now().replace(hour=8, minute=0, second=0) 
        current_time = timezone.now()
        if LegislationQuery.objects.exists():
            if ((current_time > reset_time_8am) and (reset_time_8am > LegislationQuery.objects.first().created_date_time)):
                LegislationQuery.objects.all.delete()

        # Rate limiter, so that people can't overuse the app.
        if LegislationQuery.objects.exists():
            if LegislationQuery.objects.latest('created_date_time').id >= 20:
                sorry_message = "We apologize, but the daily limit for use of the app has been exceeded. Please return tomorrow after 8am once the usage limit resets."
                html_insert = render_to_string('legislationQuery/partials/queries-and-answers.html', {'sorry_message':sorry_message})
                return HttpResponse(html_insert)


        parsed_json = json.loads(request.body)
        user_query = parsed_json.get('userQuery')
        # Sanitizes to remove HTML and JS, just as good practice, even though Django escapes HTML and JS
        user_query_sanitized = bleach.clean(user_query, tags=[], attributes={})

        # Check to prevent DB calls when user hasn't input a question. This is a redundancy in case an user disables specific JS code that prevents calls to backend.
        if user_query_sanitized == ' ':
            html_insert = render_to_string('legislationQuery/partials/queries-and-answers.html', {'user_query':user_query_sanitized,})
            return HttpResponse(html_insert)
      

        # Using async to handle simultaneous users
        client = AsyncOpenAI(
        api_key=os.environ.get('OPEN_API_KEY'),
        # Sets custom timeout settings via open ai's httpx client. 
        timeout=httpx.Timeout(70.0),
        )

      
        async def main():
            chat_completion = await client.chat.completions.create(
            messages=[
                {'role': 'user', 'content': user_query_sanitized},
                {'role': 'system', 'content': '''You are a lawyer writing a research memo. Only provide a list of legislation (i.e. statutes, regulations and by-laws) relevant to the legal issue. 
                 Answer questions in this format: - **Title of Legislation**, <br> **Summary** "Summary explained here", <br> **Relevance** "Relevance explained here". Include lots of legislation.
                 Do not answer any questions that aren't related to providing legislation. Ask for a jurisdiction if one isn't provided. '''},
            ],
            model='gpt-4o-2024-08-06',
            temperature=0.2,

            )

            return chat_completion.choices[0].message.content
        
        answer_from_gpt = asyncio.run(main())
  
        html_answer_processed = markdown.markdown(answer_from_gpt)
        # saves queries and answers to objects. len > 300 because 300 is a safe approximation of the maximum char length of an answer that does not provide legislation.
        if len(html_answer_processed) > 300:
            LegislationQuery.objects.create(query=user_query_sanitized, answer=html_answer_processed)
        

     
        html_insert = render_to_string('legislationQuery/partials/queries-and-answers.html', {'user_query':user_query, 'html_answer_processed':mark_safe(html_answer_processed),})

        return HttpResponse(html_insert)