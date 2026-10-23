import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-05-15',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def summarize_records(records):
    response = client.completions.create(
        engine='text-davinci-003',
        prompt=f'Summarize the following records: {records}',
        max_tokens=100
    )
    return response.choices[0].text.strip()