import os
import openai
from typing import List

def embed_translated_segments(segments: List[str]) -> List[List[float]]:
    """
    Embeds translated segments for translation-memory search using OpenAI embeddings.
    """
    client = openai.AzureOpenAI(
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        api_version="2024-02-01",
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT")
    )
    # Assuming a specific deployment for embeddings, e.g., "text-embedding-ada-002"
    embedding_deployment_name = os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME", "text-embedding-ada-002")

    # The OpenAI embeddings API can take a list of texts (segments) in a single request
    response = client.embeddings.create(
        input=segments,
        model=embedding_deployment_name
    )

    embeddings = [data.embedding for data in response.data]
    return embeddings
