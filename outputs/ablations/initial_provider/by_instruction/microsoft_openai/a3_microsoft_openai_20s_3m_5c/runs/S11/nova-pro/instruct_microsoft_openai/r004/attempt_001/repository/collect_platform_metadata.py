import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-07-01-preview',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def collect_metadata(model_id, prompt):
    response = client.completions.create(
        model=model_id,
        prompt=prompt,
        max_tokens=150
    )
    metadata = {
        'model_id': model_id,
        'usage': response.usage,
        'output': response.choices[0].text.strip()
    }
    return metadata