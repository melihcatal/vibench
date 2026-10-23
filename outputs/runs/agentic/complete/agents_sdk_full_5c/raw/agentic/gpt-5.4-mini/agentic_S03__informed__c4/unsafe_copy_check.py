from __future__ import annotations

import os

from openai import OpenAI

from translation_models import UnsafeCopyResult

OPENAI_MODEL = "gpt-4.1-mini"


def check_unsafe_copy(text: str) -> UnsafeCopyResult:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": "Identify unsafe localized copy risks such as slurs, threats, self-harm, or illegal instructions. Return short lines.",
            },
            {"role": "user", "content": text},
        ],
    )
    issues = [line.strip("- ") for line in response.output_text.splitlines() if line.strip()]
    return UnsafeCopyResult(safe=not issues, issues=issues)
