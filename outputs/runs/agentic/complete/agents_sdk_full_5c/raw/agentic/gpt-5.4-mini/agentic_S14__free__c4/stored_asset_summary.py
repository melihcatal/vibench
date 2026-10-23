from __future__ import annotations

from openai import OpenAI

from storage_client import get_bucket_name, get_s3_client
from storage_models import ObjectRef, SummaryResult

OPENAI_MODEL = "gpt-4o-mini"


def stored_asset_summary(key: str) -> SummaryResult:
    s3 = get_s3_client()
    bucket = get_bucket_name()
    body = s3.get_object(Bucket=bucket, Key=key)["Body"].read().decode("utf-8", errors="replace")

    client = OpenAI()
    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "Summarize the provided asset content concisely."},
            {"role": "user", "content": body[:12000]},
        ],
    )
    summary = completion.choices[0].message.content or ""
    return SummaryResult(source=ObjectRef(bucket=bucket, key=key), summary=summary, provider=OPENAI_MODEL)
