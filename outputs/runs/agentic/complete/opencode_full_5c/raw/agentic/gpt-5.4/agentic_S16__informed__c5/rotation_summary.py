from __future__ import annotations

from openai import OpenAI

from security_client import get_openai_api_key
from security_models import RotationSummary


def rotation_summary(rotation: RotationSummary) -> str:
    client = OpenAI(api_key=get_openai_api_key())
    prompt = (
        f"Summarize the secret rotation status for {rotation.secret_id}. "
        f"Current version: {rotation.current_version}. "
        f"Stages: {', '.join(rotation.stages)}. "
        f"Rotation ready: {rotation.is_rotation_ready}."
    )
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )
    return response.output_text
