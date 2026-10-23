from embeddings_client import DirectEmbeddingsClient


def multilingual_query_translate(query, target_language, config=None):
    client = DirectEmbeddingsClient(config)
    translated_query = client.translate_query(query, target_language)
    return {"translated_query": translated_query}