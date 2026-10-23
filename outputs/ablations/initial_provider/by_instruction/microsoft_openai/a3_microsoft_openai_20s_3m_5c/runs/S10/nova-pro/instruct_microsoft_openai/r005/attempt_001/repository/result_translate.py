import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-03-15-preview',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def translate_result(text: str, target_language: str) -> str:
    response = client.completions.create(
        model='text-davinci-003',
        prompt=f'Translate the following text to {target_language}: {text}',
        max_tokens=150
    )
    return response.choices[0].text.strip()