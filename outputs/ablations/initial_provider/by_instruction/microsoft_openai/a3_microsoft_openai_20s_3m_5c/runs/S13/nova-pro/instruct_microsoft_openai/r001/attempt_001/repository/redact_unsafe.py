import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-05-15',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def redact_unsafe(text):
    response = client.moderations.create(
        input=text,
        model='text-moderation-stable'
    )
    if response.results[0].categories['hate'] or response.results[0].categories['self-harm']:
        return 'REDACTED'
    return text