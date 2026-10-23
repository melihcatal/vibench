import os
from openai import AzureOpenAI

def stream_platform_generation(prompt: str, deployment_id: str):
    client = AzureOpenAI(
        api_version="2024-02-01",
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        api_key=os.environ.get("AZURE_OPENAI_API_KEY")
    )

    response_stream = client.chat.completions.create(
        model=deployment_id,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        stream=True
    )

    for chunk in response_stream:
        yield chunk
