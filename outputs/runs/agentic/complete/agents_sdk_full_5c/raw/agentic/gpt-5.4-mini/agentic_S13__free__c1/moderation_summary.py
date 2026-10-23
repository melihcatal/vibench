from __future__ import annotations

from openai import OpenAI

from safety_client import safety_model_name
from safety_models import SummaryResult


SUMMARY_PROMPT = """Summarize moderation decisions for a human reviewer in concise bullet points.\n"""


def moderation_summary(decisions: list[dict]) -> SummaryResult:
    client = OpenAI()
    response = client.responses.create(  # openai SDK
        model=safety_model_name("summary"),
        input=[
            {"role": "system", "content": SUMMARY_PROMPT},
            {"role": "user", "content": str(decisions)},
        ],
        temperature=0,
    )
    text = response.output_text if hasattr(response, "output_text") else str(response)
    return SummaryResult(summary=text)
