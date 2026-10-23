import json

from security_client import load_openai_client, provider_model, secret_identifier, system_prompt
from security_models import SecretRequest, normalize_payload


def rotate_secret_version(secret_name: str, stage: str | None = None, version: str | None = None) -> dict:
    client = load_openai_client()
    request = SecretRequest(name=secret_name, version=version, stage=stage)
    completion = client.responses.create(
        model=provider_model(),
        input=[
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": f"Read secret version for {secret_identifier(request)} and return JSON with rotation metadata."},
        ],
    )
    return normalize_payload(json.loads(completion.output_text))
