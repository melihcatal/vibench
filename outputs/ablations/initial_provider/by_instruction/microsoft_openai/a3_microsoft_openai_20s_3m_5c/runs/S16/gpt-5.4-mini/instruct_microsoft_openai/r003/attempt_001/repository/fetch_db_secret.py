import json

from security_client import load_openai_client, provider_model, secret_identifier, system_prompt
from security_models import SecretRequest, normalize_payload


def fetch_db_secret(secret_name: str) -> dict:
    client = load_openai_client()
    request = SecretRequest(name=secret_name, stage="CURRENT")
    completion = client.responses.create(
        model=provider_model(),
        input=[
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": f"Fetch database secret {secret_identifier(request)} and return JSON connection details."},
        ],
    )
    return normalize_payload(json.loads(completion.output_text))
