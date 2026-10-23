from typing import List
from embeddings_client import get_openai_client, get_embedding_model
from embeddings_models import cosine_similarity


SYSTEM_TRANSLATION_PROMPT = (
    "You are a professional translator. Translate the following text to English. "
    "Return only the translated text with no additional commentary."
)


def translate_query(
    query: str, source_language: str = "auto", target_language: str = "en"
) -> str:
    client = get_openai_client()

    if source_language != "auto":
        system_prompt = (
            f"You are a professional translator. Translate the following text from {source_language} "
            f"to {target_language}. Return only the translated text with no additional commentary."
        )
    else:
        system_prompt = SYSTEM_TRANSLATION_PROMPT

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
        temperature=0.0,
        max_tokens=512,
    )

    translated = response.choices[0].message.content.strip()
    return translated


def multilingual_search(
    query: str,
    documents: List[str],
    source_language: str = "auto",
    top_k: int = 5,
) -> List[dict]:
    translated_query = translate_query(query, source_language=source_language)

    client = get_openai_client()
    model = get_embedding_model()

    all_texts = [translated_query] + documents

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

    return {
        "original_query": query,
        "translated_query": translated_query,
        "results": top_results,
    }


if __name__ == "__main__":
    import json

    query = "机器学习的基本概念"
    documents = [
        "Machine learning is a subset of artificial intelligence",
        "Python is a popular programming language",
        "Deep learning uses neural networks with many layers",
        "The weather forecast predicts rain tomorrow",
    ]
    results = multilingual_search(query, documents, source_language="zh", top_k=2)
    print(json.dumps(results, indent=2, ensure_ascii=False))
