import os
from openai import AzureOpenAI
from typing import List

def embed_platform_output(text: str, deployment_id: str) -> List[float]:
    client = AzureOpenAI(
        api_version="2024-02-01",
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        api_key=os.environ.get("AZURE_OPENAI_API_KEY")
    )

    response = client.embeddings.create(
        model=deployment_id,
        input=text
    )

    return response.data[0].embedding
