from model_client import client


def extract_json(text: str) -> Dict[str, Any]:
    response = client.extract_json(text)
    return response.json
