import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def redact_unsafe(text):
    response = openai.Moderation.create(input=text)
    if response.results[0].flagged:
        return '[REDACTED]'
    return text