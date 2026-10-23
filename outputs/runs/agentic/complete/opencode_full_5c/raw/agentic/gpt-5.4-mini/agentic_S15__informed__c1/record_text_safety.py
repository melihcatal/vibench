from typing import Any, Dict

from openai import OpenAI


def assess_record_safety(
    record: Dict[str, Any], model: str = "gpt-5.4-mini"
) -> Dict[str, Any]:
    client = OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Assess user-generated document text for unsafe content and return a short verdict.",
            },
            {"role": "user", "content": str(record)},
        ],
    )
    return {"verdict": response.choices[0].message.content or "", "model": model}
