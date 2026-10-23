from openai import OpenAI

from security_client import build_client, model_name
from security_models import normalize_text, wrap_result


def sign_or_verify_key(message: str, signature: str = None, key_id: str = None) -> str:
    client: OpenAI = build_client()
    action = "verify" if signature else "sign"
    prompt = f"{action.title()} using the managed OpenAI model {model_name()} and key reference {key_id or 'default'}: message={normalize_text(message)} signature={normalize_text(signature)}"
    response = client.responses.create(model=model_name(), input=prompt)
    text = normalize_text(getattr(response, "output_text", ""))
    return wrap_result(text, operation="sign_or_verify_key", provider="openai", model=model_name()).result
