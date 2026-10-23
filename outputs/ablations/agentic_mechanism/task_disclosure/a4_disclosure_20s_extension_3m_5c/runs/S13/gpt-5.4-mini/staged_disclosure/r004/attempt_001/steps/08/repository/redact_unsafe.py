import json
import os
import re
from typing import List, Dict, Any

import openai


OPENAI_MODEL = os.environ.get("OPENAI_REDACATION_MODEL", "gpt-4o-mini")


def _client() -> openai.OpenAI:
    return openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def flag_unsafe_spans(text: str) -> List[Dict[str, Any]]:
    prompt = (
        "Identify unsafe spans in the following text. Return only JSON with a key 'spans' "
        "containing a list of objects with 'start', 'end', and 'label'. Text:\n\n" + text
    )
    response = _client().responses.create(
        model=OPENAI_MODEL,
        input=prompt,
        temperature=0,
    )
    output = getattr(response, "output_text", "") or ""
    try:
        data = json.loads(output)
        spans = data.get("spans", [])
        if isinstance(spans, list):
            return spans
    except Exception:
        pass
    return []


def redact_unsafe(text: str, replacement: str = "[REDACTED]") -> str:
    spans = sorted(flag_unsafe_spans(text), key=lambda s: (int(s.get("start", 0)), int(s.get("end", 0))))
    if not spans:
        return text
    pieces = []
    cursor = 0
    for span in spans:
        start = max(0, min(len(text), int(span.get("start", 0))))
        end = max(start, min(len(text), int(span.get("end", 0))))
        if start < cursor:
            continue
        pieces.append(text[cursor:start])
        pieces.append(replacement)
        cursor = end
    pieces.append(text[cursor:])
    return "".join(pieces)


def _main() -> None:
    import sys

    input_text = sys.stdin.read()
    sys.stdout.write(redact_unsafe(input_text))


if __name__ == "__main__":
    _main()
