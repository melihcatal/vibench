import os
from typing import Any, Dict

from openai import OpenAI


def onboarding_summary(event: Dict[str, Any]) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))
    model = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")
    prompt = str(event.get("state", "")).strip()
    response = client.responses.create(
        model=model, input=f"Summarize onboarding state for support: {prompt}"
    )
    return {"summary": response.output_text}
