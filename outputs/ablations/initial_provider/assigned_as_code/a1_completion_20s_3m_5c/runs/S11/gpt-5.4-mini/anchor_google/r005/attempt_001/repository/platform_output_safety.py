from google import genai

from model_client import get_platform_config
from model_models import normalize_generation_payload


def platform_output_safety(payload, config=None):
    config = get_platform_config(config)
    request = normalize_generation_payload(payload)
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        response = client.models.generate_content(model=request["model"], contents=request["text"])
    text = response.text or ""
    unsafe = any(term in text.lower() for term in ["violence", "hate", "self-harm"])
    return {"safe": not unsafe, "text": text, "model": request["model"]}
