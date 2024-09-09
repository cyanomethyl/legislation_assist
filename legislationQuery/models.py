from django.db import models

# Create your models here.

# store queries so user can see past queries they made, and the results
class LegislationQuery():
    query = models.TextField(max_length=150)
    answer = models.TextField(max_length=50)
    # This appends the string "explicitly reason through each step when providing your answer" to the query sent to OpenAI's API. This takes advantage of how LLMs work.
    # LLMs can't "go back" to their previous output, and so providing the LLM with more time to "build up" to its answer (i.e. its context window can spend more tokens focused
    # on smaller, simpler parts of the answer) allows it to provide a superior answer. Temperature is also modified separately.
    increaseAccuracy = models.BooleanField(default=False)
    # Jurisdiction is a field required separately, because most lawyers, most of the time, deal with only one jurisdiction, and so this prevents them
    # from having to mention the jurisdiction, or be prompted by gpt4o for the jurisdiction each time they ask a question (assuming it's not saving the user's preferences/past input to gpt4o session).
    # Occasionally a lawyer may want to reference out of jurisdiction legislation, for academic, publication, or legal practice purposes (e.g. looking to see how other jurisdictions treat a legal issue/s. Sometimes
    # courts will cite out of jurisdiction legislation.)
    jurisdiction = models.CharField(max_length=50)
    # Repealed legislation may be helpful in some contexts, e.g. where a lawyer is looking for clarification on an esoteric legal issue. In force legislation may not offer sufficiently helpful insight, and so sometimes lawyers turn to old legislation even if repealed.
    repealed_legislation = models.BooleanField(default=False)
    created_date_time = models.DateTimeField(auto_now_add=True)
    



