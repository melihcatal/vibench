from typing import Any, Dict

from openai import OpenAI


def invoice_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    client = OpenAI()
    text = str(payload)
    completion = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "system", "content": "Summarize invoice extraction output."}, {"role": "user", "content": text}])
    return {"summary": completion.choices[0].message.content}
