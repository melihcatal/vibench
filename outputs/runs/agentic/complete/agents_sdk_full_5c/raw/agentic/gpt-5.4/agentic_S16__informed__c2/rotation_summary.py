from __future__ import annotations

import os

from anthropic import Anthropic

from security_client import describe_secret
from security_models import RotationStatus


ANTHROPIC_MODEL = "claude-3-5-haiku-20241022"


def summarize_rotation(secret_id: str) -> dict:
    metadata = describe_secret(secret_id)
    version_map = metadata.get("VersionIdsToStages", {})
    current_version = None
    previous_version = None
    current_labels = ()
    previous_labels = ()
    for version_id, stages in version_map.items():
        labels = tuple(stages)
        if "AWSCURRENT" in labels:
            current_version = version_id
            current_labels = labels
        if "AWSPREVIOUS" in labels:
            previous_version = version_id
            previous_labels = labels
    status = RotationStatus(
        secret_id=secret_id,
        current_version=current_version,
        previous_version=previous_version,
        current_labels=current_labels,
        previous_labels=previous_labels,
    )
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=220,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": (
                    "Summarize this AWS Secrets Manager rotation status in 2-3 sentences and mention risks if labels are missing: "
                    + status.as_prompt_fragment()
                ),
            }
        ],
    )
    text = "".join(block.text for block in message.content if getattr(block, "type", None) == "text")
    return {
        "provider": "anthropic",
        "model": ANTHROPIC_MODEL,
        "secret_id": secret_id,
        "summary": text,
    }
