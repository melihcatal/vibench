from typing import List, Dict
from openai import OpenAI
from embeddings_client import build_embeddings_client, load_config_from_env
from embeddings_models import SearchResult, cosine_similarity


SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "pt": "Portuguese",
    "ru": "Russian",
    "ar": "Arabic",
    "hi": "Hindi",
    "it": "Italian",
}


def translate_query(query: str, source_lang: str, target_lang: str = "en") -> str:
    config = load_config_from_env()
    client: OpenAI = build_embeddings_client(api_key=config["api_key"])
    prompt = (
        f"Translate the following {SUPPORTED_LANGUAGES.get(source_lang, source_lang)} text to "
        f"{SUPPORTED_LANGUAGES.get(target_lang, target_lang)}. "
        f"Return only the translated text with no additional explanation.\n\n"
        f"Text: {query}"
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a professional translator. Return only the translation.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
        max_tokens=500,
    )
    translated = response.choices[0].message.content.strip()
    return translated


def translate_queries_batch(
    queries: List[str], source_lang: str, target_lang: str = "en"
) -> List[str]:
    config = load_config_from_env()
    client: OpenAI = build_embeddings_client(api_key=config["api_key"])
    translations = []
    for query in queries:
        translated = translate_query(query, source_lang, target_lang)
        translations.append(translated)
    return translations


def multilingual_search(
    query: str,
    documents: List[str],
    source_lang: str,
    target_lang: str = "en",
    model: str = "text-embedding-3-small",
    top_k: int = 5,
) -> List[SearchResult]:
    translated_query = translate_query(query, source_lang, target_lang)
    translated_docs = []
    for doc in documents:
        translated_doc = translate_query(doc, source_lang, target_lang)
        translated_docs.append(translated_doc)
    all_texts = [translated_query] + translated_docs
    config = load_config_from_env()
    client: OpenAI = build_embeddings_client(api_key=config["api_key"])
    response = client.embeddings.create(
        model=model,
        input=all_texts,
        encoding_format="float",
    )
    sorted_data = sorted(response.data, key=lambda x: x.index)
    query_embedding = sorted_data[0].embedding
    doc_embeddings = [item.embedding for item in sorted_data[1:]]
    results = []
    for i, (orig_doc, trans_doc, doc_emb) in enumerate(
        zip(documents, translated_docs, doc_embeddings)
    ):
        score = cosine_similarity(query_embedding, doc_emb)
        results.append(
            SearchResult(
                query=query,
                document=orig_doc,
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


def detect_language(text: str) -> str:
    config = load_config_from_env()
    client: OpenAI = build_embeddings_client(api_key=config["api_key"])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Detect the language of the given text. Return only the ISO 639-1 language code (e.g., en, es, fr, de, zh, ja).",
            },
            {"role": "user", "content": f"Detect the language: {text[:500]}"},
        ],
        temperature=0.0,
        max_tokens=10,
    )
    lang_code = response.choices[0].message.content.strip().lower()
    return lang_code


if __name__ == "__main__":
    query_es = "¿Qué es el aprendizaje automático?"
    docs_es = [
        "El aprendizaje automático es una rama de la inteligencia artificial",
        "Python es un lenguaje de programación popular",
        "Las redes neuronales profundas tienen muchas capas",
    ]
    results = multilingual_search(query_es, docs_es, source_lang="es", top_k=2)
    for r in results:
        print(f"Rank {r.rank}: score={r.score:.4f} - {r.document[:60]}")
