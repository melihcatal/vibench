import openai
import os

client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def is_text_safe(text: str) -> bool:
    if not text:
        return True
    response = client.moderations.create(
        input=text,
        model='text-moderation-3.5-snapshot'
    )
    return not response.results[0].flagged
