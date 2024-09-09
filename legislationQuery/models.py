from django.db import models

# Create your models here.

# store queries so user can see past queries they made, and the results
class LegislationQuery(models.Model):
    query = models.TextField(max_length=150)
    answer = models.TextField(max_length=50)
    created_date_time = models.DateTimeField(auto_now_add=True)
    



