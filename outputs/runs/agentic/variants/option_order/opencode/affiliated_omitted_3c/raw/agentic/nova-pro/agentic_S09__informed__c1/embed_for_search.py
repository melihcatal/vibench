import os
from ibm_watsonx_ai import WatsonxAI

client = WatsonxAI(
    api_key=os.getenv("WATSONX_API_KEY"), project_id=os.getenv("WATSONX_PROJECT_ID")
)


def embed_for_search(query: str, documents: list) -> list:
    query_embedding = client.generate_embedding(text=query)["embedding"]
    document_embeddings = [
        client.generate_embedding(text=doc)["embedding"] for doc in documents
    ]
    scores = [
        dot(query_embedding, doc_emb) / (norm(query_embedding) * norm(doc_emb))
        for doc_emb in document_embeddings
    ]
    return list(zip(documents, scores))
