import os

def get_openai_api_key():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return key

def get_perspective_api_key():
    key = os.getenv("PERSPECTIVE_API_KEY")
    if not key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set")
    return key
