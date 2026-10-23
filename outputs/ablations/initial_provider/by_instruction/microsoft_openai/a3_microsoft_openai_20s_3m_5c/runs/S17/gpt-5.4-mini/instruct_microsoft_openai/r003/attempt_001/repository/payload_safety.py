from openai import OpenAI

from security_client import build_client, model_name
from security_models import normalize_text, wrap_result


def payload_safety(payload: str) -> str:
    client: OpenAI = build_client()
    prompt = f"Assess whether this decrypted payload is unsafe using OpenAI model {model_name()}: {normalize_text(payload)}"
    response = client.responses.create(model=model_name(), input=prompt)
    text = normalize_text(getattr(response, "output_text", ""))
    return wrap_result(text, operation="payload_safety", provider="openai", model=model_name()).result
