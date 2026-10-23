from google import genai


def normalize_request(payload):
    return {"contents": payload["text"]}


def normalize_response(response):
    return {"text": response.text or ""}