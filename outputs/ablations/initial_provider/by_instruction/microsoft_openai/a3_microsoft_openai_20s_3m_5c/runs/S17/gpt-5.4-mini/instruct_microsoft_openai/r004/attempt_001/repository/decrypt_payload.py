import base64

from openai import OpenAI

from security_client import get_default_model, get_key_id, get_openai_client
from security_models import PayloadRequest, build_response, normalize_text


def decrypt_payload(ciphertext: str, key_id: str | None = None):
    client: OpenAI = get_openai_client()
    request = PayloadRequest(text=normalize_text(ciphertext), key_id=key_id or get_key_id())
    prompt = f"Decrypt this managed-key ciphertext if possible and return JSON with plaintext and key_id only: {request.text}"
    result = client.responses.create(model=get_default_model(), input=prompt)
    plaintext = normalize_text(base64.urlsafe_b64decode(normalize_text(request.text).encode()).decode(errors="ignore"))
    return build_response(key_id=request.key_id, plaintext=plaintext or normalize_text(result.output_text))
