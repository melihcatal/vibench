import os
from openai import AzureOpenAI

def invoke_platform_model(prompt: str, deployment_id: str):
    client = AzureOpenAI(
        api_version="2024-02-01",
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        api_key=os.environ.get("AZURE_OPENAI_API_KEY")
    )

    response = client.chat.completions.create(
        model=deployment_id,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
