from google import genai

from model_client import load_platform_config


def select_platform_resource(payload, config=None):
    config = load_platform_config(config)
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        model = payload.get("model") or config["model"]
        response = client.models.generate_content(model=model, contents=payload["text"])
    return {"model": model, "text": response.text or ""}
