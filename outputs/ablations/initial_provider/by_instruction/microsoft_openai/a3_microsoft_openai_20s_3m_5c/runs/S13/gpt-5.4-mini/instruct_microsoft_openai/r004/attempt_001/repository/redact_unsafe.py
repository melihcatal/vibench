from openai import OpenAI

from safety_client import default_moderation_model, get_client, map_category_scores
from safety_models import RedactionResult, RedactionSpan, normalize_text


def redact_unsafe(text: str) -> RedactionResult:
    client: OpenAI = get_client()
    content = normalize_text(text)
    response = client.moderations.create(model=default_moderation_model(), input=content)
    result = response.results[0]
    spans = []
    if bool(result.flagged):
        for idx, (category, flagged) in enumerate(dict(result.categories).items()):
            if flagged:
                spans.append(RedactionSpan(start=0, end=len(content), label=str(category)))
    redacted = content
    if spans:
        redacted = "[REDACTED]"
    return RedactionResult(text=redacted, spans=spans, flagged=bool(result.flagged))
