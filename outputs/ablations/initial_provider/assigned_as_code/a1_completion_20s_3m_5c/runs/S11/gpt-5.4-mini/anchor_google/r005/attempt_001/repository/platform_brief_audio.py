from google import genai

from model_client import get_platform_config
from model_models import normalize_generation_payload


def platform_brief_audio(payload, config=None):
    config = get_platform_config(config)
    request = normalize_generation_payload(payload)
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        response = client.models.generate_content(model=request["model"], contents=f"Create a spoken briefing: {request['text']}")
    return {"text": response.text or "", "audio": None, "model": request["model"]}
