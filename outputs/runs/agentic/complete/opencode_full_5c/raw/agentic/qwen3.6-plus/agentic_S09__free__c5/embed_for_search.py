from typing import List, Dict
from openai import OpenAI
from embeddings_client import build_embeddings_client, load_config_from_env
from embeddings_models import SearchResult, cosine_similarity


def embed_for_search(
    query: str,
    documents: List[str],
    model: str = "text-embedding-3-small",
    top_k: int = None,
) -> List[SearchResult]:
    config = load_config_from_env()
    client: OpenAI = build_embeddings_client(api_key=config["api_key"])
    all_texts = [query] + documents
    response = client.embeddings.create(
        model=model,
        input=all_texts,
        encoding_format="float",
    )
    sorted_data = sorted(response.data, key=lambda x: x.index)
    query_embedding = sorted_data[0].embedding
    doc_embeddings = [item.embedding for item in sorted_data[1:]]
    results = []
    for i, (doc, doc_emb) in enumerate(zip(documents, doc_embeddings)):
        score = cosine_similarity(query_embedding, doc_emb)
        results.append(
            SearchResult(
                query=query,
                document=doc,
                score=score,
                rank=0,
                embedding=doc_emb,
            )
        )
    results.sort(key=lambda r: r.score, reverse=True)
    for rank, result in enumerate(results, 1):
        result.rank = rank
    if top_k is not None:
        results = results[:top_k]
    return results


def embed_query_and_documents(
    query: str,
    documents: List[str],
    model: str = "text-embedding-3-small",
) -> Dict:
    config = load_config_from_env()
    client: OpenAI = build_embeddings_client(api_key=config["api_key"])
    query_response = client.embeddings.create(
        model=model,
        input=query,
        encoding_format="float",
    )
    query_embedding = query_response.data[0].embedding
    doc_response = client.embeddings.create(
        model=model,
        input=documents,
        encoding_format="float",
    )
    sorted_docs = sorted(doc_response.data, key=lambda x: x.index)
    doc_embeddings = [item.embedding for item in sorted_docs]
    return {
        "query_embedding": query_embedding,
        "document_embeddings": doc_embeddings,
        "model": model,
    }


if __name__ == "__main__":
    query = "What is machine learning?"
    docs = [
        "Machine learning is a branch of AI focused on algorithms that learn from data",
        "Python is a versatile programming language used in web development",
        "Deep learning uses neural networks with many layers",
        "The weather today is sunny and warm",
    ]
    results = embed_for_search(query, docs, top_k=3)
    for r in results:
        print(f"Rank {r.rank}: score={r.score:.4f} - {r.document[:60]}...")
