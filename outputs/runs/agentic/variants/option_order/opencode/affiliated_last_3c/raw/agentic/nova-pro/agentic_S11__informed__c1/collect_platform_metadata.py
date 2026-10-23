import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2023-05-15",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)


def collect_metadata(deployment_id, prompt):
    response = client.chat.completions.create(
        model=deployment_id, messages=[{"role": "user", "content": prompt}]
    )
    return {
        "output": response.choices[0].message.content,
        "usage": response.usage,
        "model_id": deployment_id,
    }
