from openai import OpenAI
from embeddings_client import get_openai_client
from embeddings_models import OPENAI_EMBEDDING_MODEL
from embed_text import embed_text


TRANSLATION_MODEL = "gpt-4o-mini"
TRANSLATION_SYSTEM_PROMPT = (
    "You are a professional translator. Translate the following text to English. "
    "Return only the translated text with no additional commentary."
)


def translate_query(
    query, target_language="English", model=TRANSLATION_MODEL, api_key=None
):
    client = get_openai_client(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": TRANSLATION_SYSTEM_PROMPT},
            {"role": "user", "content": f"Translate to {target_language}: {query}"},
        ],
        temperature=0.0,
        max_tokens=512,
    )
    translated = response.choices[0].message.content.strip()
    return translated


def translate_and_embed(
    query,
    target_language="English",
    embedding_model=OPENAI_EMBEDDING_MODEL,
    dimensions=1536,
    api_key=None,
):
    translated = translate_query(
        query, target_language=target_language, api_key=api_key
    )
    embedding = embed_text(
        translated, model=embedding_model, dimensions=dimensions, api_key=api_key
    )
    return {
        "original_query": query,
        "translated_query": translated,
        "target_language": target_language,
        "embedding_model": embedding_model,
        "embedding": embedding,
        "embedding_dimension": len(embedding),
    }


def multilingual_search(
    query,
    documents,
    source_language="auto",
    target_language="English",
    model=OPENAI_EMBEDDING_MODEL,
    dimensions=1536,
    top_k=None,
    api_key=None,
):
    translated_query = translate_query(
        query, target_language=target_language, api_key=api_key
    )
    from embed_for_search import embed_for_search

    results = embed_for_search(
        query=translated_query,
        documents=documents,
        model=model,
        dimensions=dimensions,
        top_k=top_k,
        api_key=api_key,
    )
    for r in results:
        r.query = f"[{source_language}->{target_language}] {translated_query}"
    return results


if __name__ == "__main__":
    import sys

    query = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "¿Cuáles son los beneficios del ejercicio?"
    )
    result = translate_and_embed(query)
    print(f"Original: {result['original_query']}")
    print(f"Translated: {result['translated_query']}")
    print(f"Embedding dimension: {result['embedding_dimension']}")
    print(f"First 5 values: {result['embedding'][:5]}")
