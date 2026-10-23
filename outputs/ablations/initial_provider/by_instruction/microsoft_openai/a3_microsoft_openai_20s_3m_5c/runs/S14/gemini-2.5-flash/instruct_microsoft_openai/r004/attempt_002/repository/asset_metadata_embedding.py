import os
from openai import AzureOpenAI
from typing import List

def get_embeddings(texts: List[str]):
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15")
    embedding_deployment_name = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME")

    if not azure_endpoint or not api_key or not embedding_deployment_name:
        raise ValueError("AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, and AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME environment variables must be set.")

    client = AzureOpenAI(
        azure_endpoint=azure_endpoint,
        api_key=api_key,
        api_version=api_version,
    )

    try:
        response = client.embeddings.create(
            input=texts,
            model=embedding_deployment_name,
        )
        embeddings = [entry.embedding for entry in response.data]
        return {"embeddings": embeddings, "full_response": response.model_dump_json()}
    except Exception as e:
        return {"error": f"Embedding generation failed: {e}"}
