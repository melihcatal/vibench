from typing import Dict

from openai import OpenAI


def metric_annotation_safety(text: str) -> Dict[str, object]:
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": "Assess if the text is unsafe or abusive."},
            {"role": "user", "content": text},
        ],
    )
    content = completion.choices[0].message.content or ""
    unsafe = any(token in content.lower() for token in ["unsafe", "abusive", "harmful"])
    return {"unsafe": unsafe, "analysis": content}
