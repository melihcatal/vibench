import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-05-15',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def moderate_batch(texts):
    responses = []
    for text in texts:
        response = client.moderations.create(
            input=text,
            model='text-moderation-stable'
        )
        responses.append(response.results[0].categories)
    return responses