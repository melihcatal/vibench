import json

from safety_client import build_prompt, get_google_client, get_model_name, get_threshold, make_decision, parse_categories
from safety_models import normalize_text


def moderate_text(text):
    client = get_google_client()
    model = client.GenerativeModel(get_model_name())
    prompt = build_prompt(normalize_text(text))
    response = model.generate_content(prompt)
    payload = {}
    try:
        payload = json.loads(response.text)
    except Exception:
        payload = {"allowed": True, "categories": {}}
    categories = parse_categories(payload)
    allowed = bool(payload.get("allowed", True)) and max(categories.values(), default=0.0) < get_threshold()
    return make_decision(allowed, categories, payload)
