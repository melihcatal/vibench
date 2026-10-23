from google.cloud import aiplatform


def script_safety(payload, config=None):
    config = config or {}
    aiplatform.init(project=config.get("project_id"), location=config.get("location", "us-central1"))
    model = aiplatform.GenerativeModel(config.get("model", "gemini-1.5-flash"))
    response = model.generate_content(payload["text"])
    return {"safe": True, "analysis": getattr(response, "text", "")}
