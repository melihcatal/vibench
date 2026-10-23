from google import genai


def stream_platform_generation(payload, config=None):
    config = config or {}
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        stream = client.models.generate_content_stream(model=config.get("model", "gemini-2.5-flash"), contents=payload["text"])
        chunks = []
        for chunk in stream:
            chunks.append(chunk)
    return {"stream": chunks, "text": "".join(getattr(chunk, "text", "") or "" for chunk in chunks)}
