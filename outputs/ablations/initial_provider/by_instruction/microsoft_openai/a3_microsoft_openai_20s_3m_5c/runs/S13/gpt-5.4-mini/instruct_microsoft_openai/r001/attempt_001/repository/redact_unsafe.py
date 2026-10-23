from safety_client import DEFAULT_MODERATION_MODEL, get_client, get_model
from safety_models import RedactionResult, normalize_text


def redact_unsafe(text, model=None):
    value = normalize_text(text)
    client = get_client()
    moderation_model = get_model(model, DEFAULT_MODERATION_MODEL)
    response = client.moderations.create(model=moderation_model, input=value)
    result = response.results[0]
    spans = []
    if getattr(result, "category_scores", None):
        for category, score in result.category_scores.items():
            if float(score) >= 0.5:
                spans.append({"category": category, "score": float(score)})
    redacted_text = value
    if spans:
        redacted_text = "[REDACTED]"
    return RedactionResult(redacted_text=redacted_text, spans=spans, allowed=not bool(result.flagged), raw=response.model_dump())
