from typing import Any, Dict

from openai import OpenAI


def onboarding_summary(state: str) -> Dict[str, Any]:
    client = OpenAI()
    response = client.responses.create(model="gpt-5.4-mini", input=f"Summarize this onboarding state for support: {state}")
    return {"summary": response.output_text}
