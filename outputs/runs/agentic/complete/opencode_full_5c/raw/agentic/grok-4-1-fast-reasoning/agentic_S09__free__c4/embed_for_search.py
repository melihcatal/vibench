from typing import List, Tuple
from embeddings_client import get_openai_client
from embeddings_models import Embedding, BatchEmbeddings, normalize_embedding


def embed_for_search(
    query: str, documents: List[str], model: str = "jina-embeddings-v2-base-en"
) -> Tuple[Embedding, BatchEmbeddings]:
    client = get_openai_client(base_url="https://api.jina.ai/v1")
    query_response = client.embeddings.create(model=model, input=query.strip())
    query_emb = normalize_embedding(query_response.data[0].embedding)
    docs_response = client.embeddings.create(
        model=model, input=[doc.strip() for doc in documents]
    )
    docs_embs = [normalize_embedding(item.embedding) for item in docs_response.data]
    return query_emb, docs_embs
