from translation_client import TranslationClient

def embed_translated_segments(segments):
    client = TranslationClient()
    embeddings = []
    for segment in segments:
        embedding = client.get_translation_embedding(segment)
        embeddings.append(embedding)
    return embeddings