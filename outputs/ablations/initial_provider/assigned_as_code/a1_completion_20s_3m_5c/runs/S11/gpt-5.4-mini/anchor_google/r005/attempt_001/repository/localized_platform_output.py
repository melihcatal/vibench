from google import genai

from model_client import get_platform_config
from model_models import normalize_generation_payload


def localized_platform_output(payload, config=None):
    config = get_platform_config(config)
    request = normalize_generation_payload(payload)
    target_locale = (payload or {}).get("locale") or "es"
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        response = client.models.generate_content(model=request["model"], contents=f"Translate to {target_locale}: {request['text']}")
    return {"text": response.text or "", "locale": target_locale, "model": request["model"]}
