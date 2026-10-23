import json

from security_client import load_openai_client, provider_model, secret_identifier, system_prompt
from security_models import SecretRequest, normalize_payload


def parse_json_secret(secret_name: str, version: str | None = None) -> dict:
    client = load_openai_client()
    request = SecretRequest(name=secret_name, version=version)
    completion = client.responses.create(
        model=provider_model(),
        input=[
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": f"Fetch JSON secret {secret_identifier(request)} and return the parsed object."},
        ],
    )
    return normalize_payload(json.loads(completion.output_text))
