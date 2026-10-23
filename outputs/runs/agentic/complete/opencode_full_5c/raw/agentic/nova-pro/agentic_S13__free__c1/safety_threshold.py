import safety_client


def apply_threshold(text, threshold=0.5):
    client = safety_client.get_client()
    response = client.moderate_text(text)
    if response.get("safety_score") < threshold:
        return False
    return True
