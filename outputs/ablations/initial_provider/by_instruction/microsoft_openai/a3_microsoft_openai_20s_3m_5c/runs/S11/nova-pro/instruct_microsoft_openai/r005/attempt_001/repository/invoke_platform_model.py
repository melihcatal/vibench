import os

from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-07-01-preview',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def invoke_model(model_id, messages):
    response = client.chat.completions.create(
        model=model_id,
        messages=messages,
        stream=True
    )
    return response