import json
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def extract_document_fields(document_text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": "Extract structured fields from OCR-normalized document text and return only valid JSON.",
            },
            {
                "role": "user",
                "content": (
                    "Extract the most relevant fields from this document text. "
                    "Return a JSON object with keys such as document_type, parties, dates, amounts, "
                    "identifiers, and summary when available. Text:\n" + document_text
                ),
            },
        ],
    )
    text = getattr(response, "output_text", None)
    if not text:
        output = getattr(response, "output", [])
        chunks: List[str] = []
        for item in output:
            for content in getattr(item, "content", []) or []:
                chunk = getattr(content, "text", None)
                if chunk:
                    chunks.append(chunk)
        text = "".join(chunks)
    try:
        return json.loads(text)
    except Exception:
        return {"raw_output": text}


def main() -> None:
    import sys

    document_text = sys.stdin.read()
    result = extract_document_fields(document_text)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
