from embeddings_client import get_cohere_client


def check_corpus_safety(text: str) -> dict:
    """Checks corpus text for safety before embedding using Cohere's moderation API."""
    co = get_cohere_client()
    response = co.moderate(text=text)
    # The response object has a 'id' and 'detections' attribute.
    # Detections is a list of dictionaries, each with a 'label' and 'confidence' and 'moderation_id'
    return {"id": response.id, "detections": [d.to_dict() for d in response.detections]}
