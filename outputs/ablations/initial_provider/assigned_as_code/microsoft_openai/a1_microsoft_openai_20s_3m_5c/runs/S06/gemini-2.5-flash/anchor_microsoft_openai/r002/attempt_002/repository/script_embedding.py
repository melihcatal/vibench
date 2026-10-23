import os
import requests
from speech_models import EmbeddingPayload

# Azure OpenAI Embeddings endpoint and key
# https://learn.microsoft.com/en-us/azure/ai-services/openai/reference

def embed_script(payload: EmbeddingPayload, config: dict = None):
    api_key = config.get('api_key') or os.environ.get("AZURE_OPENAI_KEY")
    endpoint = config.get('endpoint') or os.environ.get("AZURE_OPENAI_ENDPOINT")
    deployment_name = config.get('deployment_name') or os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")

    if not api_key or not endpoint or not deployment_name:
        raise ValueError("Azure OpenAI API key, endpoint, and deployment name must be provided or set as environment variables AZURE_OPENAI_KEY, AZURE_OPENAI_ENDPOINT, and AZURE_OPENAI_EMBEDDING_DEPLOYMENT.")

    # Example endpoint: https://YOUR_RESOURCE_NAME.openai.azure.com/
    # Example deployment name: text-embedding-ada-002 (or your custom deployment name)
    url = f"{endpoint}openai/deployments/{deployment_name}/embeddings?api-version=2024-02-01"

    headers = {
        "api-key": api_key,
        "Content-Type": "application/json",
    }

    data = {
        "input": payload.text
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status() # Raise an exception for HTTP errors
        embedding_result = response.json()

        if 'data' in embedding_result and len(embedding_result['data']) > 0:
            embedding = embedding_result['data'][0]['embedding']
            return {"embedding": embedding, "model": deployment_name}
        else:
            raise RuntimeError(f"No embedding data found in response: {embedding_result}")

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error calling Azure OpenAI Embeddings API: {e}")
