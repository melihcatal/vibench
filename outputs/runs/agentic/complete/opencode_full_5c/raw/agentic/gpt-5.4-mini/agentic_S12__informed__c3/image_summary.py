from typing import Any, Dict, List

from openai import OpenAI


client = OpenAI()


def image_summary(labels: List[Dict[str, Any]], description: str, text: List[Dict[str, Any]]) -> Dict[str, Any]:
    prompt = {"labels": labels, "description": description, "text": text}
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize visual analysis results concisely."},
            {"role": "user", "content": str(prompt)},
        ],
    )
    return {"summary": response.choices[0].message.content}
