from typing import List, Dict, Tuple
from embeddings_client import get_openai_client, get_embedding_model
from embeddings_models import cosine_similarity


def embed_for_search(
    query: str,
    documents: List[str],
    top_k: int = 5,
) -> List[Dict]:
    client = get_openai_client()
    model = get_embedding_model()

    all_texts = [query] + documents

    api_response = client.embeddings.create(
        model=model,
        input=all_texts,
        encoding_format="float",
    )

    query_embedding = api_response.data[0].embedding

    scored_results = []
    for i, doc_text in enumerate(documents):
        doc_embedding = api_response.data[i + 1].embedding
        score = cosine_similarity(query_embedding, doc_embedding)
        scored_results.append(
            {
                "document": doc_text,
                "score": score,
                "rank": 0,
            }
        )

    scored_results.sort(key=lambda x: x["score"], reverse=True)
    top_results = scored_results[:top_k]

    for rank, result in enumerate(top_results, start=1):
        result["rank"] = rank

    return top_results


if __name__ == "__main__":
    import json

    query = "machine learning algorithms"
    documents = [
        "Python is a popular programming language",
        "Neural networks are a key part of deep learning",
        "The weather is sunny today",
        "Support vector machines classify data points",
        "Random forests combine decision trees for prediction",
    ]
    results = embed_for_search(query, documents, top_k=3)
    print(json.dumps(results, indent=2))
