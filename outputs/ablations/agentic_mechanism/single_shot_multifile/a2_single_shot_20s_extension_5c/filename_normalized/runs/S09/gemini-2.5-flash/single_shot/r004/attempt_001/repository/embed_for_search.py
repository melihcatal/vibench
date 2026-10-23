from typing import List, Tuple
from embeddings_client import get_openai_embedding_client, OPENAI_EMBEDDING_MODEL

def embed_for_search(query_text: str, document_texts: List[str]) -> Tuple[List[float], List[List[float]]]:
    client = get_openai_embedding_client()
    all_texts = [query_text] + document_texts
    response = client.embeddings.create(
        input=all_texts,
        model=OPENAI_EMBEDDING_MODEL
    )
    query_embedding = response.data[0].embedding
    document_embeddings = [item.embedding for item in response.data[1:]]
    return query_embedding, document_embeddings
