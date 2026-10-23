from __future__ import annotations

import json
import os
from typing import Optional

from openai import OpenAI

from security_client import get_secret_metadata, list_secret_versions
from security_models import RotationSummary


OPENAI_MODEL = "gpt-4o-mini"


def build_rotation_summary(secret_id: str, project_id: Optional[str] = None) -> RotationSummary:
    metadata = get_secret_metadata(secret_id=secret_id, project_id=project_id)
    versions = list_secret_versions(secret_id=secret_id, project_id=project_id)

    enabled = []
    disabled = []
    latest_version = None

    for version in versions:
        version_id = version.name.split("/")[-1]
        state_name = getattr(version.state, "name", str(version.state))
        if state_name == "ENABLED":
            enabled.append(version_id)
            latest_version = version_id
        else:
            disabled.append(version_id)

    return RotationSummary(
        secret_name=metadata.name,
        version_count=len(versions),
        enabled_versions=enabled,
        disabled_versions=disabled,
        latest_version=latest_version,
        labels=dict(metadata.labels),
    )


def summarize_rotation_status(secret_id: str, project_id: Optional[str] = None) -> str:
    summary = build_rotation_summary(secret_id=secret_id, project_id=project_id)
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = (
        "Summarize the following secret rotation status for an operations dashboard in 3 concise bullet points: "
        + json.dumps(summary.__dict__)
    )
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
