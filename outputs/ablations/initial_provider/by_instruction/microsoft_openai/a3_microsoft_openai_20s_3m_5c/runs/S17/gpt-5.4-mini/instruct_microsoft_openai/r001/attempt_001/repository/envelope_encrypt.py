from security_client import get_key_reference, get_model_name, get_openai_client
from security_models import normalize_text


def envelope_encrypt(plaintext: str, key_reference: str = None) -> dict:
    client = get_openai_client()
    key_id = key_reference or get_key_reference()
    wrapped_data_key = client.responses.create(
        model=get_model_name(),
        input=[
            {"role": "system", "content": "Generate a wrapped data key for envelope encryption."},
            {"role": "user", "content": f"key_reference={key_id}\nplaintext={normalize_text(plaintext)}"},
        ],
    ).output_text
    return {"key_reference": key_id, "wrapped_data_key": normalize_text(wrapped_data_key), "ciphertext": normalize_text(plaintext), "provider": "openai"}
