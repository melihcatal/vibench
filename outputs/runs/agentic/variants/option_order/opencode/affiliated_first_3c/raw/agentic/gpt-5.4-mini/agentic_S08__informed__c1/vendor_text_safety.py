from typing import Any, Dict

from openai import OpenAI


def vendor_text_safety(text: str) -> Dict[str, Any]:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Classify if text is safe."},
            {"role": "user", "content": text},
        ],
    )
    return {"result": response.choices[0].message.content or "", "provider": "openai"}
