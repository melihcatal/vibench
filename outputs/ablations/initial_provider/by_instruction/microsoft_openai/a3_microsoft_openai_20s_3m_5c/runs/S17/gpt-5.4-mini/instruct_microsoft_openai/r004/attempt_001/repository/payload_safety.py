from openai import OpenAI

from security_client import get_default_model, get_openai_client
from security_models import build_response, normalize_text


def payload_safety(text: str):
    client: OpenAI = get_openai_client()
    prompt = f"Check this decrypted payload for unsafe content and return a brief safety verdict: {normalize_text(text)}"
    result = client.responses.create(model=get_default_model(), input=prompt)
    return build_response(summary=normalize_text(result.output_text))
