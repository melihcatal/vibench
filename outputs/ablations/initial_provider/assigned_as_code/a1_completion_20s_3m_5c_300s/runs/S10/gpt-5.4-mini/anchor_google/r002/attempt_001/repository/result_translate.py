from model_client import generate_text, resolve_model
from model_models import normalize_text_response


def result_translate(payload, config=None):
    target_language = payload.get("target_language", "English")
    prompt = "Translate the following model output into " + target_language + ".\n\n" + payload["text"]
    response = generate_text(prompt, config=config, model=resolve_model(config))
    return normalize_text_response(response)
