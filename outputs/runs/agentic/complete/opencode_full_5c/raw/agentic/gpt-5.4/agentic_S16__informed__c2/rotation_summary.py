from __future__ import annotations

from security_client import get_secrets_manager_client
from security_models import summarize_rotation


def rotation_summary(secret_id: str) -> str:
    client = get_secrets_manager_client()
    metadata = client.describe_secret(SecretId=secret_id)
    summary = summarize_rotation(secret_id, metadata)
    prompt = (
        "Summarize AWS Secrets Manager rotation status for operations review. "
        f"Secret: {summary.secret_id}. "
        f"Rotation enabled: {summary.rotation_enabled}. "
        f"Current version: {summary.current_version}. "
        f"Previous version: {summary.previous_version}. "
        f"Last rotated: {summary.last_rotated_date}. "
        f"Next rotation: {summary.next_rotation_date}. "
        f"Stages: {summary.stages}."
    )
    client_llm = __import__("openai").OpenAI(
        api_key=__import__("os").environ["OPENAI_API_KEY"]
    )
    result = client_llm.responses.create(model="gpt-4.1-mini", input=prompt)
    return result.output_text
