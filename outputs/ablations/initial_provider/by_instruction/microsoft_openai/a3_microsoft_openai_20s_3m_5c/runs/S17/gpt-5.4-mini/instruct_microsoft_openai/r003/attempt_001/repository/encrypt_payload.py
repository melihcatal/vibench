from openai import OpenAI

from security_client import build_client, model_name
from security_models import PayloadRequest, normalize_text, wrap_result


def encrypt_payload(payload: str, key_id: str = None) -> str:
    client: OpenAI = build_client()
    request = PayloadRequest(payload=normalize_text(payload), key_id=key_id)
    prompt = f"Encrypt this payload using the managed OpenAI model {model_name()} and key reference {request.key_id or 'default'}: {request.payload}"
    response = client.responses.create(model=model_name(), input=prompt)
    text = normalize_text(getattr(response, "output_text", ""))
    return wrap_result(text, operation="encrypt", provider="openai", model=model_name()).result
