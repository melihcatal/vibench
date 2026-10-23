from google import genai

from model_client import load_platform_config


def stream_platform_generation(payload, config=None):
    cfg = load_platform_config(config)
    chunks = []
    with genai.Client(vertexai=True, project=cfg["project_id"], location=cfg["location"]) as client:
        stream = client.models.generate_content_stream(model=cfg["model"], contents=payload["text"])
        for chunk in stream:
            chunks.append(chunk)
    text = "".join(getattr(chunk, "text", "") or "" for chunk in chunks)
    return {"text": text, "chunks": chunks, "model": cfg["model"]}
