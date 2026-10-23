from __future__ import annotations

from google.cloud import dlp_v2

from security_client import get_secret_metadata
from security_models import collect_text_fields


def secret_label_safety(
    secret_id: str, notes: str | None = None, project_id: str | None = None
) -> dict:
    secret = get_secret_metadata(secret_id=secret_id, project_id=project_id)
    labels = dict(getattr(secret, "labels", {}) or {})
    text = "\n".join(collect_text_fields(labels, notes))
    client = dlp_v2.DlpServiceClient()
    parent = f"projects/{project_id or secret.name.split('/')[1]}/locations/global"
    response = client.inspect_content(
        request={
            "parent": parent,
            "item": {"value": text},
            "inspect_config": {
                "info_types": [
                    {"name": "API_KEY"},
                    {"name": "PASSWORD"},
                    {"name": "DATABASE_CREDENTIALS"},
                ],
                "include_quote": True,
            },
        }
    )
    findings = [
        {
            "info_type": finding.info_type.name,
            "quote": finding.quote,
            "likelihood": getattr(finding.likelihood, "name", str(finding.likelihood)),
        }
        for finding in response.result.findings
    ]
    return {
        "secret_id": secret_id,
        "labels": labels,
        "unsafe": bool(findings),
        "findings": findings,
    }
