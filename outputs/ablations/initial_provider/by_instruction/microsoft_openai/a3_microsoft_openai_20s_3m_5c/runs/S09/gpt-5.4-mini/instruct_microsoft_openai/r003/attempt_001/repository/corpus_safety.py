from embeddings_client import get_client, moderation_model


def corpus_safety(texts: list[str]) -> list[dict[str, object]]:
    client = get_client()
    results = []
    for text in texts:
        moderation = client.moderations.create(model=moderation_model(), input=text)
        results.append({"text": text, "flagged": moderation.results[0].flagged, "categories": moderation.results[0].categories})
    return results
