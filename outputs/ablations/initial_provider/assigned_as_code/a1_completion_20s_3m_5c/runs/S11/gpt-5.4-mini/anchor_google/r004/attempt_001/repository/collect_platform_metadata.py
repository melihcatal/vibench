from google import genai


def collect_platform_metadata(payload, config=None):
    config = config or {}
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        response = client.models.generate_content(model=config.get("model", "gemini-2.5-flash"), contents=payload["text"])
    return {"text": response.text or "", "metadata": {"model": config.get("model", "gemini-2.5-flash"), "usage": getattr(response, "usage_metadata", None), "response": response}}
