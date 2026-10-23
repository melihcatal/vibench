from typing import Any, Dict, List

from openai import OpenAI

from database_models import DocumentOperationResponse

MODEL_ID = "gpt-4o-mini"


def summarize_records(records: List[Dict[str, Any]]) -> DocumentOperationResponse:
    client = OpenAI()
    prompt = f"Summarize these document records concisely: {records}"
    completion = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You summarize managed NoSQL document records."},
            {"role": "user", "content": prompt},
        ],
    )
    text = completion.choices[0].message.content or ""
    return DocumentOperationResponse(ok=True, document={"summary": text}, message="summarized")


if __name__ == "__main__":
    raise SystemExit("This module exposes summarize_records() using OpenAI chat completions.")
