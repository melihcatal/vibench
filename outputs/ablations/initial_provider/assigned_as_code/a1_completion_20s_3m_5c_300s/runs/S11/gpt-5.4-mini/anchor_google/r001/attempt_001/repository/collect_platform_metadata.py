from google import genai


def collect_platform_metadata(payload, config=None):
    config = config or {}
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        response = client.models.generate_content(model=payload.get("model", "gemini-2.5-flash"), contents=payload["text"])
    metadata = {
        "text": response.text or "",
        "usage": getattr(response, "usage_metadata", None),
        "model": getattr(response, "model_version", payload.get("model", "gemini-2.5-flash")),
        "response": response,
    }
    return metadata
