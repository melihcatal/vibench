import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-05-15',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def select_model():
    models = client.models.list()
    for model in models.data:
        if model.id.startswith('text-davinci'):
            return model.id
    return None