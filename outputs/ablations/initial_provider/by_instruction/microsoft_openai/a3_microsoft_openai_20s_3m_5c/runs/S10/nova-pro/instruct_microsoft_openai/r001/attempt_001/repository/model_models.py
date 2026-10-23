from.model_client import get_client

def normalize_response(response):
    return response.choices[0].text.strip()