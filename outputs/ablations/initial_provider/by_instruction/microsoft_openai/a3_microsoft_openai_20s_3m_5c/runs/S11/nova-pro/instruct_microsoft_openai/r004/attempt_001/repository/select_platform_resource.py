import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-07-01-preview',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def select_model():
    model_list = client.models.list()
    model_ids = [model.id for model in model_list.data]
    return model_ids[0] if model_ids else None