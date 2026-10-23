import os
from openai import AzureOpenAI
from embeddings_models import EmbeddingResponse

def embed_for_search(query_text: str, document_texts: list[str]) -> tuple[EmbeddingResponse, list[EmbeddingResponse]]:
    """Embeds a query and documents for semantic search using Azure OpenAI.
    Returns the query embedding and a list of document embeddings."""
    client = AzureOpenAI(
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),  
        api_version="2023-05-15",
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT")
    )
    
    deployment_name = os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME") # This will be the `deployment_name` you chose for your model

    # Embed query
    query_response = client.embeddings.create(
        input=[query_text],
        model=deployment_name # model parameter is the deployment name for Azure OpenAI
    )
    query_embedding = EmbeddingResponse(text=query_text, embedding=query_response.data[0].embedding, model=deployment_name)

    # Embed documents
    document_embeddings = []
    if document_texts:
        doc_response = client.embeddings.create(
            input=document_texts,
            model=deployment_name
        )
        for i, doc_text in enumerate(document_texts):
            document_embeddings.append(EmbeddingResponse(text=doc_text, embedding=doc_response.data[i].embedding, model=deployment_name))

    return query_embedding, document_embeddings