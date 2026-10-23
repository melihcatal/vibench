from typing import Any, Dict, List

from openai import OpenAI

OPENAI_MODEL = "gpt-4o-mini"


def onboarding_summary(state: Dict[str, Any]) -> str:
    client = OpenAI()
    prompt = {
        "account_state": state.get("account_state"),
        "locale": state.get("locale"),
        "moderation": state.get("moderation"),
        "notes": state.get("notes", []),
        "events": state.get("events", []),
    }
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "Summarize onboarding state for support in a compact, factual way."},
            {"role": "user", "content": str(prompt)},
        ],
        temperature=0.1,
    )
    return response.choices[0].message.content or ""
