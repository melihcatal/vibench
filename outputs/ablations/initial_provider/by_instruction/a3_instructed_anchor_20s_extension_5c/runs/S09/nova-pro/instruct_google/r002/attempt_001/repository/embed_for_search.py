from google.cloud import texttospeech

def embed_for_search(query, documents):
    client = texttospeech.TextToSpeechClient()
    query_embedding = embed_text(query)
    document_embeddings = embed_batch(documents)
    return query_embedding, document_embeddings