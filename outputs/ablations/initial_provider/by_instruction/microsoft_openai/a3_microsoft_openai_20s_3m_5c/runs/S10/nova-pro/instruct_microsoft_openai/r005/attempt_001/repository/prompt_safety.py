import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-03-15-preview',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def check_prompt_safety(prompt: str) -> bool:
    response = client.completions.create(
        model='text-davinci-003',
        prompt=f'Check if the following prompt is safe: {prompt}',
        max_tokens=5
    )
    return 'safe' in response.choices[0].text.lower()