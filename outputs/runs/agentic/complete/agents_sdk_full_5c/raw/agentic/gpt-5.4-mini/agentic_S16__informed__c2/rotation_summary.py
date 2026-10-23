from __future__ import annotations

from openai import OpenAI

from security_models import RotationSummary

MODEL_ID = "gpt-4o-mini"


def summarize_rotation(summary: RotationSummary) -> str:
    client = OpenAI()
    prompt = (
        f"Summarize secret rotation status for {summary.secret_id}. "
        f"Current={summary.current_version}, Previous={summary.previous_version}, "
        f"Staged={summary.staged_label}, Rotated={summary.rotated}."
    )
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You summarize operational secret rotation status succinctly."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content or ""
