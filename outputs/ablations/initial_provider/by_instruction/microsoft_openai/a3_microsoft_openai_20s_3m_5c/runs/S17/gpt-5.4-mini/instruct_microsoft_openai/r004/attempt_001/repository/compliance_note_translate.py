from openai import OpenAI

from security_client import get_default_model, get_openai_client
from security_models import build_response, normalize_text


def compliance_note_translate(text: str, target_language: str = "English"):
    client: OpenAI = get_openai_client()
    prompt = f"Translate this encryption or compliance note into {target_language}: {normalize_text(text)}"
    result = client.responses.create(model=get_default_model(), input=prompt)
    return build_response(summary=normalize_text(result.output_text))
