from openai import OpenAI

from security_client import get_default_model, get_openai_client
from security_models import build_response, normalize_text


def key_usage_summary(events: list[str]):
    client: OpenAI = get_openai_client()
    prompt = "Summarize these key usage and crypto events for compliance review: " + " | ".join(normalize_text(e) for e in events)
    result = client.responses.create(model=get_default_model(), input=prompt)
    return build_response(summary=normalize_text(result.output_text))
