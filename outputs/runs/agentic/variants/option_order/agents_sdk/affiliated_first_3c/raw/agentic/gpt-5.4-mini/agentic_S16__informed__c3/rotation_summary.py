from __future__ import annotations

import os
from typing import Iterable

from openai import OpenAI

from security_models import RotationStatus

OPENAI_MODEL = "gpt-4.1-mini"


def summarize_rotation(statuses: Iterable[RotationStatus]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = "Summarize the secret rotation status of these entries:\n" + "\n".join(
        f"- {s.secret_name}: active={s.active_version}, previous={s.previous_version}, staged={s.staged_version}, note={s.description}" for s in statuses
    )
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
