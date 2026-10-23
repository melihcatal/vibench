import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-05-15',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def translate_text(text, target_language):
    response = client.completions.create(
        model='text-davinci-003',
        prompt=f'Translate the following text to {target_language}: {text}',
        max_tokens=200
    )
    return response.choices[0].text.strip()