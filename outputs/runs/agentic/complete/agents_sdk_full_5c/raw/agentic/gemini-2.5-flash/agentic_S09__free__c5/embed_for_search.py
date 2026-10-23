import os
from google.cloud import aiplatform

# Initialize Vertex AI client
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")
LOCATION = os.getenv("GCP_LOCATION", "us-central1")
aiplatform.init(project=PROJECT_ID, location=LOCATION)

def embed_for_search(query: str, documents: list[str]) -> tuple[list[float], list[list[float]]]:
    """
    Embeds a query and a list of documents for semantic search using Vertex AI.

    Args:
        query: The search query string.
        documents: A list of document strings to embed.

    Returns:
        A tuple containing:
        - The embedding vector for the query.
        - A list of embedding vectors, one for each document.
    """
    model = aiplatform.Endpoint.from_pretrained(
        "text-embedding-gecko@001" # Concrete model identifier
    )

    all_texts = [query] + documents
    instances = [{"content": text} for text in all_texts]
    response = model.predict(instances=instances)

    all_embeddings = []
    if response.predictions:
        for prediction in response.predictions:
            if 'embeddings' in prediction:
                all_embeddings.append(prediction['embeddings']['values'])

    query_embedding = all_embeddings[0] if all_embeddings else []
    document_embeddings = all_embeddings[1:] if len(all_embeddings) > 1 else []

    return query_embedding, document_embeddings

if __name__ == '__main__':
    search_query = "latest advancements in artificial intelligence"
    corpus_documents = [
        "Artificial intelligence (AI) is intelligence demonstrated by machines.",
        "Machine learning is a subset of AI that involves training algorithms.",
        "Deep learning is a subfield of machine learning inspired by the human brain.",
        "Recent breakthroughs in large language models have transformed AI capabilities."
    ]

    query_emb, doc_embs = embed_for_search(search_query, corpus_documents)

    print(f"Query embedding (first 5 dim): {query_emb[:5]}...")
    print(f"Number of document embeddings: {len(doc_embs)}")
    if doc_embs:
        print(f"First document embedding (first 5 dim): {doc_embs[0][:5]}...")
