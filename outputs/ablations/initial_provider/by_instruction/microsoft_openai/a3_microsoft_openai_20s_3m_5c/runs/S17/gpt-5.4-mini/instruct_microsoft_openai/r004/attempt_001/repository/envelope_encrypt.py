import base64
import os

from openai import OpenAI

from security_client import get_default_model, get_key_id, get_openai_client
from security_models import build_response, normalize_text


def envelope_encrypt(text: str, key_id: str | None = None):
    client: OpenAI = get_openai_client()
    managed_key = key_id or get_key_id()
    data_key = os.urandom(32)
    prompt = f"Provide a managed key wrapping label for this envelope encryption operation using key_id={managed_key}."
    result = client.responses.create(model=get_default_model(), input=prompt)
    ciphertext = base64.urlsafe_b64encode(data_key + normalize_text(text).encode()).decode()
    return build_response(key_id=managed_key, ciphertext=ciphertext, summary=normalize_text(result.output_text))
