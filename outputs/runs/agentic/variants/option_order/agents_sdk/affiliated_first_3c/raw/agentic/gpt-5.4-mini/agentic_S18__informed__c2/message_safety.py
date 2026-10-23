from typing import Dict

from openai import OpenAI

from messaging_models import normalize_text


MODEL_ID = "gpt-4o-mini"


def check_message_safety(payload: Dict[str, object]) -> Dict[str, object]:
    text = normalize_text(payload.get("text") or payload.get("body") or payload.get("message"))
    client = OpenAI()
    completion = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "Classify the text as safe or unsafe and provide a brief reason."},
            {"role": "user", "content": text},
        ],
        temperature=0.0,
    )
    verdict = completion.choices[0].message.content if completion.choices else "safe"
    return {"text": text, "verdict": verdict, "model": MODEL_ID}
