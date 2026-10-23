from openai import OpenAI

from security_client import build_client, model_name
from security_models import normalize_text, wrap_result


def compliance_note_translate(note: str, target_language: str = "en") -> str:
    client: OpenAI = build_client()
    prompt = f"Translate this encryption or compliance note into {normalize_text(target_language)} using OpenAI model {model_name()}: {normalize_text(note)}"
    response = client.responses.create(model=model_name(), input=prompt)
    text = normalize_text(getattr(response, "output_text", ""))
    return wrap_result(text, operation="compliance_note_translate", provider="openai", model=model_name()).result
