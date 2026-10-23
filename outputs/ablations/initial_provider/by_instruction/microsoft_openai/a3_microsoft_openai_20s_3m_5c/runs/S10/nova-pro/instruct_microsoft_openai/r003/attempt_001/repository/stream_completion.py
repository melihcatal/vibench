import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-05-15',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def stream_completion(prompt):
    response = client.completions.create(
        model='text-davinci-003',
        prompt=prompt,
        max_tokens=150,
        stream=True
    )
    for chunk in response:
        yield chunk.choices[0].text.strip()