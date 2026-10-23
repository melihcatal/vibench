from safety_client import get_safety_client

def safety_threshold(text, thresholds):
    client = get_safety_client()
    response = client.moderate(text)
    for category, score in response['categories'].items():
        if score > thresholds.get(category, 0):
            return False
    return True