"""Summarize secret rotation status using OpenAI chat completions."""

import os
import json
from typing import Any
from openai import OpenAI


def summarize_rotation_status(
    rotation_events: list[dict[str, Any]],
    model: str = "gpt-4o-mini",
) -> str:
    """Generate a summary of secret rotation events using OpenAI.

    Args:
        rotation_events: A list of rotation event dicts with keys like
            'secret_name', 'provider', 'old_version', 'new_version',
            'rotated_at', 'status', 'notes'.
        model: OpenAI model identifier, defaults to 'gpt-4o-mini'.

    Returns:
        A human-readable summary of the rotation status.

    Raises:
        ValueError: If OPENAI_API_KEY is not set.
        Exception: If the OpenAI API call fails.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    events_json = json.dumps(rotation_events, indent=2, default=str)

    system_prompt = (
        "You are a security operations assistant. Summarize the provided "
        "secret rotation events. Highlight any failures, secrets that have "
        "not been rotated recently, and overall rotation health. "
        "Keep the summary concise (under 200 words)."
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Rotation events:\n{events_json}"},
        ],
        temperature=0.3,
        max_tokens=500,
    )

    summary = response.choices[0].message.content or ""
    return summary


if __name__ == "__main__":
    sample_events = [
        {
            "secret_name": "db-password",
            "provider": "aws",
            "old_version": "v1",
            "new_version": "v2",
            "rotated_at": "2025-01-10T12:00:00Z",
            "status": "completed",
            "notes": "Routine quarterly rotation",
        },
        {
            "secret_name": "api-token",
            "provider": "azure",
            "old_version": "v5",
            "new_version": None,
            "rotated_at": "2025-01-09T08:00:00Z",
            "status": "failed",
            "notes": "Downstream service unreachable",
        },
    ]
    result = summarize_rotation_status(sample_events)
    print(result)
