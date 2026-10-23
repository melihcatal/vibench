import os
import json
from model_client import ManagedModelClient
from model_models import InvocationRequest, InvocationResponse
import openai

def platform_output_embedding(text: str) -> dict:
    """
    Embed platform model output for evaluation or retrieval using a provider embedding model.
    This example uses OpenAI's embedding endpoint (provider SDK). Adjust model name for other providers.
    """
    client = ManagedModelClient()
    embedding = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    # The response contains a list of embeddings; we extract the first one
    vector = embedding.data[0].embedding
    return {
        "text": text,
        "embedding": vector,
        "dimension": len(vector)
    }

if __name__ == "__main__":
    sample = "Managed Model Platform Workflow is powerful."
    emb = platform_output_embedding(sample)
    print("Embedding for sample:", json.dumps(emb, indent=2))