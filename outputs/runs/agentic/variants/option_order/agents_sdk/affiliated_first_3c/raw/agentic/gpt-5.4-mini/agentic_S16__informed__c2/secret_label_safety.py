from __future__ import annotations

import os
from typing import Dict

from openai import OpenAI


MODEL_ID = "gpt-4.1-mini"


def check_label_safety(label: str, note: str) -> Dict[str, str]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = f"Assess whether this secret label or note is unsafe, suspicious, or leaks sensitive data. Label: {label}\nNote: {note}"
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "Return a concise safety assessment."},
            {"role": "user", "content": prompt},
        ],
    )
    return {"assessment": response.choices[0].message.content or "", "label": label}


def main() -> Dict[str, str]:
    label = os.environ.get("SECRET_LABEL", "production-db-password")
    note = os.environ.get("SECRET_NOTE", "Rotated after quarterly review.")
    return check_label_safety(label, note)


if __name__ == "__main__":
    print(main())
