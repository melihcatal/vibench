import safety_client


def moderate_batch(messages):
    client = safety_client.get_client()
    results = []
    for message in messages:
        response = client.moderate_text(message)
        results.append(response.get("safety_score"))
    return results
