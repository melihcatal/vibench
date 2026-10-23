import os
from google.cloud import language_v1
from google.cloud import translate_v2 as translate

def embed_translated_segments(translated_texts: list[str]) -> list[dict]:
    """Embed translated segments using Google Cloud Natural Language embedding API for translation memory search.",
    """
    client = translate.Client()  # re-use translation client for credentials
    language_client = language_v1.LanguageServiceClient()
    embeddings = []
    for text in translated_texts:
        # Get embedding (pseudo-code; actual API may use a different method)
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        embedding = language_client.get_document_embedding(document=document)
        embeddings.append({'text': text, 'embedding': embedding['embedding']})
    return embeddings