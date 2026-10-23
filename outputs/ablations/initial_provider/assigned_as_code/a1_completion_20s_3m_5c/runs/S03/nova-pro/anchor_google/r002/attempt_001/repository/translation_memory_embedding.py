from google.cloud import translate_v3

from translation_client import get_translation_client


def embed_translation_memory(translations, config=None):
    config = config or {}
    client = get_translation_client(config)
    parent = f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"
    response = client.embed_translation_memory(request={
        "parent": parent,
        "translations": translations,
   })
    embeddings = []
    for embedding in response.embeddings:
        embeddings.append({
            "text": embedding.text,
            "embedding": embedding.embedding,
       })
    return embeddings