from openai import OpenAI

from security_client import build_client, model_name
from security_models import normalize_text, wrap_result


def key_usage_summary(events: str) -> str:
    client: OpenAI = build_client()
    prompt = f"Summarize key usage and crypto events with OpenAI model {model_name()}: {normalize_text(events)}"
    response = client.responses.create(model=model_name(), input=prompt)
    text = normalize_text(getattr(response, "output_text", ""))
    return wrap_result(text, operation="key_usage_summary", provider="openai", model=model_name()).result
