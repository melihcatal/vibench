from embeddings_client import DEFAULT_CHAT_MODEL, get_client


def corpus_safety(texts: list[str]) -> dict[str, object]:
    client = get_client()
    response = client.responses.create(model=DEFAULT_CHAT_MODEL, input=f"Check this corpus for safety issues and return JSON: {texts}")
    return {'provider': 'openai', 'assessment': response.output_text}
