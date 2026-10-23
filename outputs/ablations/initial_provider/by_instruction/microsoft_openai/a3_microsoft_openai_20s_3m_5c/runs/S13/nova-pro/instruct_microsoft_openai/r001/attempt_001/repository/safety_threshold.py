import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-05-15',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def safety_threshold(text, threshold=0.5):
    response = client.moderations.create(
        input=text,
        model='text-moderation-stable'
    )
    if response.results[0].categories['hate'] > threshold:
        return False
    return True