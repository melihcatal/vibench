import os
from openai import AzureOpenAI

def embed_query_and_docs_azure_openai(
    query: str,
    documents: list[str],
    azure_deployment_id: str
) -> tuple[list[float], list[list[float]]]:
    """
    Embeds a query and a list of documents for semantic search using Azure OpenAI.
    The `azure_deployment_id` typically maps to a specific embedding model.
    """
    client = AzureOpenAI(
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        api_version="2024-02-01"
    )
    
    all_texts = [query] + documents
    try:
        response = client.embeddings.create(input=all_texts, model=azure_deployment_id)
        all_embeddings = [item.embedding for item in response.data]
        
        query_embedding = all_embeddings[0]
        document_embeddings = all_embeddings[1:]
        
        return query_embedding, document_embeddings
    except Exception as e:
        print(f"Error embedding texts with Azure OpenAI: {e}")
        return [], []
