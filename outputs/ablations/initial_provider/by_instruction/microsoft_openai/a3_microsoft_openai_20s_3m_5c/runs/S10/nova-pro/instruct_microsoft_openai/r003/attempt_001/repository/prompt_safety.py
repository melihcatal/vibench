import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-05-15',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def check_safety(text):
    response = client.completions.create(
        model='text-davinci-003',
        prompt=f'Check if the following text contains unsafe content: {text}',
        max_tokens=50
    )
    return response.choices[0].text.strip()