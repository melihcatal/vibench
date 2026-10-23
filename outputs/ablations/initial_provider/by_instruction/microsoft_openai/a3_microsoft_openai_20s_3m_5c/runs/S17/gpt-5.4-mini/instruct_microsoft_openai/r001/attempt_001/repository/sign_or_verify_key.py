from security_client import get_key_reference, get_model_name, get_openai_client
from security_models import normalize_text


def sign_or_verify_key(payload: str, mode: str = "sign", key_reference: str = None) -> dict:
    client = get_openai_client()
    key_id = key_reference or get_key_reference()
    result = client.responses.create(
        model=get_model_name(),
        input=[
            {"role": "system", "content": f"Perform {mode} operation for a managed key and return a concise result."},
            {"role": "user", "content": f"key_reference={key_id}\npayload={normalize_text(payload)}"},
        ],
    ).output_text
    return {"mode": mode, "key_reference": key_id, "result": normalize_text(result), "provider": "openai"}
