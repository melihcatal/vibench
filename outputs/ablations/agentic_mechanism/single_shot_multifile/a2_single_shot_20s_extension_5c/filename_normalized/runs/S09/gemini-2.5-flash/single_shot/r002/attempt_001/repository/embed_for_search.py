import os
from typing import List, Dict, Any

from openai import AzureOpenAI

def embed_for_search(query: str, documents: List[str]) -> Dict[str, List[List[float]]]:
    client = AzureOpenAI(
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        api_version="2024-02-01"
    )

    deployment_name = os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")

    query_response = client.embeddings.create(
        input=query,
        model=deployment_name # model maps to a deployment name in Azure OpenAI
    )
    query_embedding = [query_response.data[0].embedding]

    doc_response = client.embeddings.create(
        input=documents,
        model=deployment_name
    )
    doc_embeddings = [d.embedding for d in doc_response.data]

    return {
        "query_embedding": query_embedding,
        "document_embeddings": doc_embeddings
    }