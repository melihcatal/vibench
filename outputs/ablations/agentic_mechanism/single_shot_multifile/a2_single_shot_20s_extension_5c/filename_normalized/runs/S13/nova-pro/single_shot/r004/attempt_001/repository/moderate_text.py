from safety_client import get_safety_client

def moderate_text(text):
    client = get_safety_client()
    response = client.moderate(text)
    return response['categories']