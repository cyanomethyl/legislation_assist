from django.db import models

# Stores user queries, answers from GPT, and the created_date_time for rate limiting.
class LegislationQuery(models.Model):
    query = models.TextField(max_length=150)
    answer = models.TextField(max_length=50)
    created_date_time = models.DateTimeField(auto_now_add=True)
    



