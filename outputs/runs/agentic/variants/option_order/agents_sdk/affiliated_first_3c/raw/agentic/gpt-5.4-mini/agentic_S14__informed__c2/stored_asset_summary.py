from __future__ import annotations

from typing import List

from openai import OpenAI

from storage_models import SummaryRequest

client = OpenAI()
MODEL_ID = "gpt-4o-mini"


def stored_asset_summary(source_text: str, max_sentences: int = 5) -> dict:
    request = SummaryRequest(source_text=source_text, max_sentences=max_sentences)
    prompt = f"Summarize the following content in at most {request.max_sentences} sentences.\n\n{request.source_text}"
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You summarize stored asset content for downstream workflows."},
            {"role": "user", "content": prompt},
        ],
    )
    summary = response.choices[0].message.content or ""
    return {"summary": summary, "model": MODEL_ID, "sentence_limit": request.max_sentences}
