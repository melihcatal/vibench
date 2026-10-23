from embeddings_client import EmbeddingsClient

client = EmbeddingsClient()

def check_corpus_safety(text):
    # Placeholder for corpus safety check logic
    return 'Safe' if 'unsafe' not in text.lower() else 'Unsafe'