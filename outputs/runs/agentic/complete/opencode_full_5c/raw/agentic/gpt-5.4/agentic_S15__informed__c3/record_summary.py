from __future__ import annotations

import os
from typing import Any
from typing import Dict
from typing import Iterable

from openai import OpenAI

from database_models import build_summary_text


def summarize_record(
    document: Dict[str, Any], fields: Iterable[str] | None = None
) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = build_summary_text(document, fields=fields)
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize the provided NoSQL document record for an internal operations user.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.output_text
