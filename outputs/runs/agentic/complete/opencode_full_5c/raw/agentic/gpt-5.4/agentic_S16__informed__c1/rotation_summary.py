from __future__ import annotations

from security_client import get_openai_client
from security_models import RotationSummary


def summarize_rotation_status(
    secret_name: str,
    current_version: str | None,
    requested_version: str | None,
    labels: dict[str, str],
) -> RotationSummary:
    client = get_openai_client()
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize secret rotation state in one short status phrase.",
            },
            {
                "role": "user",
                "content": f"Secret: {secret_name}\nCurrent version: {current_version}\nRequested version: {requested_version}\nLabels: {labels}",
            },
        ],
    )
    status = response.output_text.strip()
    return RotationSummary(
        secret_name=secret_name,
        current_version=current_version,
        requested_version=requested_version,
        labels=dict(labels),
        status=status,
    )
