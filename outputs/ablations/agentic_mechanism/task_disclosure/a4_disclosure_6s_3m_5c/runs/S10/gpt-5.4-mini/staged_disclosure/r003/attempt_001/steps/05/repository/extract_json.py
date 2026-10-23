import json
import os
import sys
from typing import Any

from openai import OpenAI


def _build_messages(text: str, schema_hint: str) -> list[dict[str, str]]:
    user_content = (
        "Extract the requested structured JSON from the text below. "
        "Return only valid JSON and no extra text.\n\n"
        f"Schema hint: {schema_hint}\n\n"
        f"Text:\n{text}"
    )
    return [
        {
            "role": "system",
            "content": "You are a precise information extraction engine that outputs only JSON.",
        },
        {"role": "user", "content": user_content},
    ]


def extract_json(text: str, schema_hint: str = "") -> Any:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=_build_messages(text, schema_hint),
        temperature=0,
    )
    output_text = response.output_text.strip()
    return json.loads(output_text)


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: extract_json.py <text> [schema_hint]")
    text = sys.argv[1]
    schema_hint = sys.argv[2] if len(sys.argv) > 2 else ""
    result = extract_json(text, schema_hint)
    sys.stdout.write(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
