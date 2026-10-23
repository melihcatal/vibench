import json

from security_client import get_openai_client, get_secret_model, get_secret_name
from security_models import SecretResponse, normalize_secret_payload


def parse_json_secret() -> SecretResponse:
    client = get_openai_client()
    secret_name = get_secret_name("json-secret")
    model = get_secret_model()
    result = client.responses.create(
        model=model,
        input=f"Retrieve the JSON-formatted secret named {secret_name} and return it as valid JSON."
    )
    payload = normalize_secret_payload(json.loads(result.output_text))
    return SecretResponse(name=secret_name, value=payload, metadata={"model": model})
