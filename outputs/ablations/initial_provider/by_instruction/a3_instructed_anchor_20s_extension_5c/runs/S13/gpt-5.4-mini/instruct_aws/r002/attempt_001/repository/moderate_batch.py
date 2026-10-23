from safety_client import summarize_comprehend_moderation
from safety_models import normalize_messages


def moderate_batch(messages):
    outputs = []
    for message in normalize_messages(messages):
        decision = summarize_comprehend_moderation(message)
        outputs.append({"message": message, "allow": decision.allow, "categories": decision.categories, "provider": decision.provider})
    return outputs
