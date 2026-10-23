from openai import OpenAI

from security_client import build_client, model_name
from security_models import normalize_text, wrap_result


def crypto_audit_embedding(note: str) -> str:
    client: OpenAI = build_client()
    prompt = f"Create a semantic embedding-oriented audit note using OpenAI model {model_name()}: {normalize_text(note)}"
    response = client.responses.create(model=model_name(), input=prompt)
    text = normalize_text(getattr(response, "output_text", ""))
    return wrap_result(text, operation="crypto_audit_embedding", provider="openai", model=model_name()).result
