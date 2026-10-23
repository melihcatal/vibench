from translation_client import client

def embed_translated_segments(text: str) -> str:
    response = client.translations.embed_segments(text)
    return response['embedding']