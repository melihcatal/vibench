def normalize_text_input(text):
    return text.strip() if isinstance(text, str) else str(text)


def normalize_text_list(texts):
    return [normalize_text_input(text) for text in texts]


def _extract_vector(item):
    return item.embedding if hasattr(item, "embedding") else item["embedding"]


def single_embedding_response(response):
    return _extract_vector(response.data[0])


def batch_embedding_response(response):
    return [_extract_vector(item) for item in response.data]
