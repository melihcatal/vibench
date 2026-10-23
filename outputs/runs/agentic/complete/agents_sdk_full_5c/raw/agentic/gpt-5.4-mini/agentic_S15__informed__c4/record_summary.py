from typing import Any, Dict

from openai import OpenAI

MODEL_ID = "gpt-4o-mini"


def summarize_record(record: Dict[str, Any]) -> Dict[str, Any]:
    client = OpenAI()
    prompt = f"Summarize this document record in 1-2 sentences:\n{record}"
    completion = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You summarize document records concisely."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return {"provider": "OpenAI", "model": MODEL_ID, "summary": completion.choices[0].message.content}
