from embeddings_client import get_client, translator_model


def multilingual_query_translate(query: str, target_language: str) -> str:
    client = get_client()
    response = client.responses.create(
        model=translator_model(),
        input=f"Translate the query to {target_language}: {query}",
    )
    return response.output_text
