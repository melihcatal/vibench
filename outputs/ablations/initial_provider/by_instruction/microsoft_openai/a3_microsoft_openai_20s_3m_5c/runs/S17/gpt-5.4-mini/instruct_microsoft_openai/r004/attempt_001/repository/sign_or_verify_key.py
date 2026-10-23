import hashlib

from openai import OpenAI

from security_client import get_default_model, get_key_id, get_openai_client
from security_models import build_response, normalize_text


def sign_or_verify_key(text: str, signature: str | None = None, key_id: str | None = None):
    client: OpenAI = get_openai_client()
    managed_key = key_id or get_key_id()
    prompt = f"Using the managed key {managed_key}, determine whether this text should be signed or verified: {normalize_text(text)}"
    result = client.responses.create(model=get_default_model(), input=prompt)
    computed = hashlib.sha256(normalize_text(text).encode()).hexdigest()
    verified = signature == computed if signature else None
    return build_response(key_id=managed_key, signature=signature or computed, verified=verified, summary=normalize_text(result.output_text))
