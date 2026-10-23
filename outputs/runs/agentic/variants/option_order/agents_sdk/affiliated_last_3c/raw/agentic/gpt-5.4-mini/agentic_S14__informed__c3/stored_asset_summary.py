from __future__ import annotations

from openai import OpenAI

from storage_models import AssetSummaryResult, StorageObjectRef


SUMMARY_MODEL = "gpt-4o-mini"


def stored_asset_summary(bucket: str, key: str, extracted_text: str, metadata: dict | None = None) -> AssetSummaryResult:
    client = OpenAI()
    prompt = f"Summarize this asset. Metadata: {metadata or {}}\n\nText:\n{extracted_text}"
    resp = client.chat.completions.create(
        model=SUMMARY_MODEL,
        messages=[
            {"role": "system", "content": "You summarize stored asset content succinctly."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    summary = resp.choices[0].message.content or ""
    return AssetSummaryResult(source=StorageObjectRef(bucket=bucket, key=key), summary=summary, provider="openai", tags=[])
