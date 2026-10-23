from embeddings_client import load_config


def corpus_safety(texts):
    config = load_config()
    unsafe = [text for text in texts if not text or len(text.strip()) == 0]
    return {"provider": "openai", "model": config.model, "safe": len(unsafe) == 0, "rejected_count": len(unsafe)}
