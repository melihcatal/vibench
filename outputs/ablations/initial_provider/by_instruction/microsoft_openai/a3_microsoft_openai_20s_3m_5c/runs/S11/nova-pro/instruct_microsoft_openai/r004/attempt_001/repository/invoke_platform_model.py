import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-07-01-preview',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def invoke_model(model_id, prompt):
    response = client.completions.create(
        model=model_id,
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()