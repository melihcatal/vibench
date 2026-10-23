import os

from google import genai


DEFAULT_MODEL = "gemini-2.5-flash"


def resolve_api_key(config=None):
    config = config or {}
    return config.get("api_key") or os.environ["GOOGLE_API_KEY"]


def resolve_model(config=None, default=DEFAULT_MODEL):
    config = config or {}
    return config.get("model") or default


def create_client(config=None):
    return genai.Client(api_key=resolve_api_key(config))


def generate_text(prompt, config=None, model=None):
    config = config or {}
    model = model or resolve_model(config)
    with create_client(config) as client:
        response = client.models.generate_content(model=model, contents=prompt)
    return response


def stream_text(prompt, config=None, model=None):
    config = config or {}
    model = model or resolve_model(config)
    with create_client(config) as client:
        for chunk in client.models.generate_content_stream(model=model, contents=prompt):
            yield chunk
