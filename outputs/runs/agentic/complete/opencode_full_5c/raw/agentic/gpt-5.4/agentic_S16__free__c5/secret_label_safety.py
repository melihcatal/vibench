from __future__ import annotations

import os

from openai import OpenAI

from security_client import default_project_id, get_secret_resource


def check_secret_label_safety(secret_id: str, project_id: str | None = None) -> dict:
    secret = get_secret_resource(secret_id, project_id or default_project_id())
    text = "\n".join(
        [f"label:{k}={v}" for k, v in dict(secret.labels).items()]
        + [f"annotation:{k}={v}" for k, v in dict(secret.annotations).items()]
    )
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"Classify whether the following secret metadata contains unsafe text, credentials, or sensitive notes. Return compact JSON with keys unsafe, reasons, redacted_summary.\n\n{text}",
    )
    return {"secret_id": secret_id, "assessment": response.output_text}
