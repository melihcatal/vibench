def normalize_texts(payload):
    texts = payload.get("texts")
    if texts is None:
        text = payload.get("text")
        return [text] if text is not None else []
    return list(texts)


def normalize_embedding(values):
    return list(values)


def unpack_embeddings(response):
    return [normalize_embedding(item.values) for item in response.embeddings]
