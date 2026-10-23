from google import genai


def select_platform_resource(config=None):
    config = config or {}
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        model_name = config.get("model", "gemini-2.5-flash")
        response = client.models.get(model=model_name)
    return {"model": model_name, "resource": response}
