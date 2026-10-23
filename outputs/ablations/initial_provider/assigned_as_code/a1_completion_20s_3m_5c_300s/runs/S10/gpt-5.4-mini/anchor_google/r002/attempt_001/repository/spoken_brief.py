from model_client import generate_text
from model_models import normalize_text_response


def spoken_brief(payload, config=None):
    prompt = "Rewrite the following model output as a short spoken brief.\n\n" + payload["text"]
    response = generate_text(prompt, config=config, model="gemini-2.5-flash")
    return normalize_text_response(response)
