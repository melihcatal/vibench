import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-05-15',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def redact_unsafe(text):
    response = client.completions.create(
        model='text-moderation-001',
        prompt=text,
        max_tokens=100
    )
    redacted_text = response.choices[0].text
    return redacted_text