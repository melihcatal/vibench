from embeddings_client import DEFAULT_TRANSLATION_MODEL, get_client


def multilingual_query_translate(query: str, target_language: str) -> str:
    client = get_client()
    response = client.responses.create(model=DEFAULT_TRANSLATION_MODEL, input=f"Translate the query to {target_language}: {query}")
    return response.output_text
