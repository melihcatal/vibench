from .safety_client import create_client, moderate_text


def moderate_batch(messages):
    client = create_client()
    results = []
    for message in messages:
        result = moderate_text(client, message)
        results.append(result)
    return results
