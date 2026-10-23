from embeddings_client import EmbeddingsClient

client = EmbeddingsClient()


def translate_query(query: str, target_language: str) -> str:
    response = client.translate_text(query, target_language)
    return response["translated_text"]
