from security_client import get_key_reference, get_model_name, get_openai_client
from security_models import PayloadRequest, PayloadResponse, normalize_text


def decrypt_payload(ciphertext: str, key_reference: str = None) -> PayloadResponse:
    client = get_openai_client()
    request = PayloadRequest(plaintext=normalize_text(ciphertext), key_reference=key_reference or get_key_reference())
    response = client.responses.create(
        model=get_model_name(),
        input=[
            {
                "role": "system",
                "content": "Decrypt the provided ciphertext using the managed key reference and return plaintext only.",
            },
            {
                "role": "user",
                "content": f"key_reference={request.key_reference}\nciphertext={request.plaintext}",
            },
        ],
    )
    plaintext = normalize_text(getattr(response, "output_text", ""))
    return PayloadResponse(ciphertext=plaintext, key_reference=request.key_reference, provider="openai")
