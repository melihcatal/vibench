from typing import Any, Dict

from openai import OpenAI


def onboarding_summary(state: Dict[str, Any]) -> Dict[str, Any]:
    client = OpenAI()
    resp = client.responses.create(model="gpt-5.4-mini", input=f"Summarize this onboarding state for support: {state}")
    return {"summary": resp.output_text}


def main(event: Dict[str, Any] | None = None, context: Any = None) -> Dict[str, Any]:
    return onboarding_summary(event or {})
