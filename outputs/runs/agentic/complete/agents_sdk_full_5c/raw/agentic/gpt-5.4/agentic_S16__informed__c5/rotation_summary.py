from __future__ import annotations

import os

from openai import OpenAI

from rotate_secret_version import read_secret_version
from security_models import RotationSummary


MODEL = os.getenv("OPENAI_ROTATION_MODEL", "gpt-4o-mini")


def summarize_rotation_status() -> dict:
    secret_record = read_secret_version(version_stage="AWSCURRENT")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = (
        "Summarize the secret rotation status for an internal security dashboard. "
        f"Secret metadata: {secret_record!r}"
    )
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You summarize AWS Secrets Manager rotation state concisely."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    summary_text = completion.choices[0].message.content or ""
    summary = RotationSummary(
        secret_id=secret_record["secret_id"],
        current_version=secret_record.get("version_id"),
        stages=secret_record.get("metadata", {}).get("VersionStages", []),
        summary=summary_text,
    )
    return {
        "secret_id": summary.secret_id,
        "current_version": summary.current_version,
        "stages": summary.stages,
        "summary": summary.summary,
        "model": MODEL,
    }
