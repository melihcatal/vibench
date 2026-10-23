from google.cloud import aiplatform


def crypto_audit_embedding(text: str) -> dict:
    aiplatform.init(project=None, location="us-central1")
    return {"provider": "google_vertex_ai", "embedding_source": "textembedding-gecko@003", "text": text}
