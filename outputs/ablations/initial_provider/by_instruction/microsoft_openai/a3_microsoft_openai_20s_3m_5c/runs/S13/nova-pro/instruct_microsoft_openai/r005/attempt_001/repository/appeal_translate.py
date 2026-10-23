import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-05-15',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def translate_appeal(text):
    response = client.completions.create(
        model='text-translation-001',
        prompt=text,
        max_tokens=100
    )
    return response.choices[0].text