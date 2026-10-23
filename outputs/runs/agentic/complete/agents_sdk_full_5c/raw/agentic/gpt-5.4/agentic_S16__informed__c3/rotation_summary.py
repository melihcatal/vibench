from __future__ import annotations

from openai import OpenAI

from security_client import get_secrets_manager_client, require_secret_id
from security_models import normalize_rotation_metadata


OPENAI_MODEL = "gpt-4o-mini"


def rotation_summary(secret_id: str | None = None) -> str:
    sm_client = get_secrets_manager_client()
    resolved_secret_id = secret_id or require_secret_id("ROTATION_SECRET_ID")
    metadata = sm_client.describe_secret(SecretId=resolved_secret_id)
    summary = normalize_rotation_metadata(metadata, resolved_secret_id)

    prompt = (
        f"Summarize AWS Secrets Manager rotation health for secret {summary.secret_id}. "
        f"Rotation enabled: {summary.rotation_enabled}. "
        f"Last rotated: {summary.last_rotated_date}. "
        f"Next rotation: {summary.next_rotation_date}. "
        f"Version stages: {summary.version_ids_to_stages}."
    )

    client = OpenAI()
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt,
    )
    return response.output_text
