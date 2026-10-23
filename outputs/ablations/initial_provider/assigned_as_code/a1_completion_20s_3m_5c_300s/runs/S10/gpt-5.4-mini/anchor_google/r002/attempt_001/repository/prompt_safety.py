from model_client import generate_text
from model_models import normalize_text_response


def prompt_safety(payload, config=None):
    prompt = "Classify the following prompt for safety concerns and respond with a concise verdict.\n\n" + payload["text"]
    response = generate_text(prompt, config=config, model="gemini-2.5-flash")
    return normalize_text_response(response)
