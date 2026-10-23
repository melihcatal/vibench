from security_client import get_model_name, get_openai_client
from security_models import normalize_text


def payload_safety(text):
    client = get_openai_client()
    verdict = client.responses.create(
        model=get_model_name(),
        input=[
            {"role": "system", "content": "Check decrypted text payloads for unsafe content and return a risk label."},
            {"role": "user", "content": normalize_text(text)},
        ],
    ).output_text
    return {"verdict": normalize_text(verdict), "provider": "openai"}
