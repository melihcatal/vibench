from embeddings_client import get_config


def corpus_safety(payload, config=None):
    get_config(config)
    text = payload["text"]
    return {"safe": bool(text.strip()), "text": text[:1000]}
