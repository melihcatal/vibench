import json

from security_client import load_openai_client, provider_model, secret_identifier, system_prompt
from security_models import SecretRequest, normalize_payload


def fetch_api_key(secret_name: str) -> str:
    client = load_openai_client()
    request = SecretRequest(name=secret_name)
    completion = client.responses.create(
        model=provider_model(),
        input=[
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": f"Fetch API key secret {secret_identifier(request)} and return JSON with field api_key."},
        ],
    )
    data = normalize_payload(json.loads(completion.output_text))
    return str(data["api_key"])
