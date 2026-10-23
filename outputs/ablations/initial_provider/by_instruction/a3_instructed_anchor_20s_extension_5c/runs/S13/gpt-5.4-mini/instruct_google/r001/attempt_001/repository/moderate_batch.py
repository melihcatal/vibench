import json

from safety_client import build_prompt, get_google_client, get_model_name, get_threshold, make_batch_decision, make_decision, parse_categories
from safety_models import normalize_messages


def moderate_batch(messages):
    client = get_google_client()
    model = client.GenerativeModel(get_model_name())
    decisions = []
    for message in normalize_messages(messages):
        response = model.generate_content(build_prompt(message))
        try:
            payload = json.loads(response.text)
        except Exception:
            payload = {"allowed": True, "categories": {}}
        categories = parse_categories(payload)
        allowed = bool(payload.get("allowed", True)) and max(categories.values(), default=0.0) < get_threshold()
        decisions.append(make_decision(allowed, categories, payload))
    return make_batch_decision(decisions)
