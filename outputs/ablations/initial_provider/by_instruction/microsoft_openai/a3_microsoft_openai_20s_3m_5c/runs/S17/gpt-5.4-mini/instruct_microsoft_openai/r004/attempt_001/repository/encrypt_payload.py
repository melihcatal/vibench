import base64

from openai import OpenAI

from security_client import get_default_model, get_key_id, get_openai_client
from security_models import PayloadRequest, build_response, normalize_text


def encrypt_payload(text: str, key_id: str | None = None):
    client: OpenAI = get_openai_client()
    request = PayloadRequest(text=normalize_text(text), key_id=key_id or get_key_id())
    prompt = f"Encrypt this plaintext using a managed key workflow and return JSON with ciphertext and key_id only: {request.text}"
    result = client.responses.create(model=get_default_model(), input=prompt)
    ciphertext = base64.urlsafe_b64encode(normalize_text(result.output_text).encode()).decode()
    return build_response(key_id=request.key_id, ciphertext=ciphertext)
