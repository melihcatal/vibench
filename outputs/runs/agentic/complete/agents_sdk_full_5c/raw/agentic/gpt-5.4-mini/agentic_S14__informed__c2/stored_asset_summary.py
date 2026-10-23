from __future__ import annotations

from typing import Dict

from openai import OpenAI

from storage_client import load_storage_config

_MODEL_ID = "gpt-4o-mini"


def summarize_stored_asset(bucket: str, key: str, extracted_text: str) -> Dict[str, str]:
    load_storage_config(bucket)
    client = OpenAI()
    response = client.chat.completions.create(
        model=_MODEL_ID,
        messages=[
            {"role": "system", "content": "Summarize stored asset content succinctly for search indexing."},
            {"role": "user", "content": f"Bucket: {bucket}\nKey: {key}\n\n{extracted_text}"},
        ],
        temperature=0.2,
    )
    summary = response.choices[0].message.content or ""
    return {"bucket": bucket, "key": key, "model": _MODEL_ID, "summary": summary}
