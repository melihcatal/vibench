import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2023-05-15",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)


def stream_generation(deployment_id, prompt):
    response = client.chat.completions.create(
        model=deployment_id, messages=[{"role": "user", "content": prompt}], stream=True
    )
    for chunk in response:
        yield chunk.choices[0].delta.content
