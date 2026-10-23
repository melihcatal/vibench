from safety_client import get_safety_client

def moderate_batch(texts):
    client = get_safety_client()
    results = [client.moderate(text)['categories'] for text in texts]
    return results