from typing import Any, Dict

from openai import OpenAI

from identity_models import normalize_text


def onboarding_summary(state_text: str) -> Dict[str, Any]:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Summarize this onboarding state for support: {normalize_text(state_text)}",
            }
        ],
    )
    return {"summary": response.choices[0].message.content or ""}
