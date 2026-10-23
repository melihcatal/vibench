from google import genai


def select_platform_resource(payload, config=None):
    config = config or {}
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        model_name = payload.get("model") or config.get("model", "gemini-2.5-flash")
        model = client.models.get(model=model_name)
    return {"model": getattr(model, "name", model_name), "resource": model}
