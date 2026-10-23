from speech_client import build_client


def transcript_embedding(segments):
    client = build_client()
    texts = [
        getattr(s, "text", s.get("text") if isinstance(s, dict) else str(s))
        for s in segments
    ]
    return client.embeddings.create(model="text-embedding-3-large", input=texts)
