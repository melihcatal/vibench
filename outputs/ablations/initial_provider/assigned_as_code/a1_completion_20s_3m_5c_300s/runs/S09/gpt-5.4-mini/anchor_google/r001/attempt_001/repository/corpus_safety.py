def corpus_safety(payload, config=None):
    texts = payload.get("texts", [])
    blocked = [text for text in texts if any(term in text.lower() for term in ("password", "secret", "ssn"))]
    return {"safe": not blocked, "blocked_texts": blocked}
