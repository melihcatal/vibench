from typing import Any, Dict

from openai import OpenAI

from identity_client import build_identity_config


class SummaryError(RuntimeError):
    pass


def onboarding_summary(state: Dict[str, Any]) -> Dict[str, str]:
    cfg = build_identity_config()
    client = OpenAI(api_key=cfg.api_key)
    prompt = (
        "Summarize this onboarding state for support in one concise paragraph. "
        "Include blockers, completed steps, and next action. State: "
        f"{state}"
    )
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )
    summary = response.output_text if hasattr(response, "output_text") else str(response)
    return {"summary": summary, "model": "gpt-4.1-mini"}
