from __future__ import annotations

from openai import OpenAI

from rotate_secret_version import read_secret_version
from security_models import SummaryResult, summarize_rotation


OPENAI_MODEL = "gpt-4o-mini"


def rotation_summary(secret_id: str, region_name: str | None = None, version_stage: str = "AWSCURRENT") -> SummaryResult:
    secret_payload = read_secret_version(secret_id, region_name=region_name, version_stage=version_stage)
    normalized = summarize_rotation(secret_payload)
    client = OpenAI()
    prompt = (
        "Summarize the AWS Secrets Manager rotation posture in one concise paragraph. "
        f"SecretId={normalized.secret_id}; VersionId={normalized.version_id}; "
        f"Stages={normalized.stages}; Status={normalized.status}; "
        f"Recommendation={normalized.recommendation}."
    )
    response = client.responses.create(model=OPENAI_MODEL, input=prompt)
    return SummaryResult(model=OPENAI_MODEL, summary=response.output_text.strip())
