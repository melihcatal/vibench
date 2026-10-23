import os


def get_perspective_api_key():
    return os.getenv("PERSPECTIVE_API_KEY")


def create_perspective_api_headers():
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_perspective_api_key()}",
    }


def create_perspective_api_data(text):
    return {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
