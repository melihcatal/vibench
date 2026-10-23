def local_request(text: str) -> dict:
    return {"text": text}


def local_response(response: dict) -> str:
    return response.get('safety_result', '')


def normalize_text(text: str) -> str:
    return text.strip().lower()