from embeddings_client import create_embeddings_client, handle_embedding_error
from embeddings_models import (
    EmbeddingRequest,
    EmbeddingResponse,
    batch_cosine_similarities,
)

TRANSLATION_MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"


def translate_query(query, target_language="en", client=None, api_key=None):
    if client is None:
        client, _ = create_embeddings_client(model=EMBEDDING_MODEL, api_key=api_key)

    system_prompt = (
        "You are a translation assistant. Translate the user's query to "
        f"{target_language}. Return only the translated text with no explanation."
    )

    try:
        response = client.chat.completions.create(
            model=TRANSLATION_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query},
            ],
            temperature=0.0,
            max_tokens=512,
        )
        translated = response.choices[0].message.content.strip()
        return translated
    except Exception as exc:
        handle_embedding_error(exc)


def multilingual_query_translate(
    query,
    documents,
    source_language=None,
    target_language="en",
    model=None,
    client=None,
    api_key=None,
    top_k=None,
):
    if not query or not query.strip():
        raise ValueError("query must be a non-empty string")
    if not documents:
        raise ValueError("documents list must not be empty")

    if client is None:
        client, model = create_embeddings_client(model=model, api_key=api_key)

    if model is None:
        model = EMBEDDING_MODEL

    if source_language and source_language.lower() != target_language.lower():
        translated_query = translate_query(
            query, target_language=target_language, client=client, api_key=api_key
        )
    else:
        translated_query = query

    all_texts = [translated_query] + list(documents)

    request = EmbeddingRequest(
        texts=all_texts,
        model=model,
    )

    try:
        response = client.embeddings.create(**request.to_payload())
        result = EmbeddingResponse.from_openai_response(response)
    except Exception as exc:
        handle_embedding_error(exc)

    query_vec = result.get_embedding(0)
    doc_vecs = [result.get_embedding(i + 1) for i in range(len(documents))]

    similarities = batch_cosine_similarities(query_vec, doc_vecs)

    scored_docs = []
    for idx, (doc, score) in enumerate(zip(documents, similarities)):
        scored_docs.append(
            {
                "document": doc,
                "similarity_score": score,
                "index": idx,
            }
        )

    scored_docs.sort(key=lambda x: x["similarity_score"], reverse=True)

    if top_k is not None:
        scored_docs = scored_docs[:top_k]

    return {
        "original_query": query,
        "translated_query": translated_query,
        "source_language": source_language,
        "target_language": target_language,
        "results": scored_docs,
        "model": model,
        "total_documents": len(documents),
        "usage": result.usage,
    }
