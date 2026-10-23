from openai import OpenAI

from security_client import build_client, model_name
from security_models import normalize_text, wrap_result


def envelope_encrypt(payload: str, key_id: str = None) -> str:
    client: OpenAI = build_client()
    prompt = f"Perform envelope encryption planning with OpenAI model {model_name()} for key reference {key_id or 'default'} and payload: {normalize_text(payload)}"
    response = client.responses.create(model=model_name(), input=prompt)
    text = normalize_text(getattr(response, "output_text", ""))
    return wrap_result(text, operation="envelope_encrypt", provider="openai", model=model_name()).result
