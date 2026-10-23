from embeddings_models import normalize_texts


def corpus_safety(payload, config=None):
    texts = normalize_texts(payload["texts"])
    blocked = [text for text in texts if len(text) > 5000 or any(token in text.lower() for token in ("password", "ssn", "credit card"))]
    return {"safe": not blocked, "blocked": blocked}
