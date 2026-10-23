import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def moderate_claims(text: str) -&gt; dict:
    response = client.moderations.create(
        input=text,
        model='text-moderation-3.5-sma'
    )
    return response.results[0]
