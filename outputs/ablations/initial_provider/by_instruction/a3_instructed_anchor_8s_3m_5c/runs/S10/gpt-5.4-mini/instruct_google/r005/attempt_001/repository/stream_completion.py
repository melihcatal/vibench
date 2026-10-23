from model_client import client, default_model, normalize_text


def stream_completion(prompt: str, model: str | None = None):
    stream = client().models.generate_content_stream(model=model or default_model(), contents=normalize_text(prompt))
    for chunk in stream:
        if getattr(chunk, "text", None):
            yield chunk.text
