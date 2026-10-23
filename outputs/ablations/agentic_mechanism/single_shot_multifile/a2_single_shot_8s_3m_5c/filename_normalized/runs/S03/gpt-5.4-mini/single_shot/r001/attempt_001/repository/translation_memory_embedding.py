from translation_client import get_translation_client

_PROVIDER = "google"


def translation_memory_embedding(text: str) -> list:
    client = get_translation_client()
    return client.embed_translation(text)
