import os
from typing import Any, Dict, Iterable

from openai import OpenAI

from safety_client import get_openai_client


def moderation_summary(decisions: Iterable[Dict[str, Any]]) -> str:
    client: OpenAI = get_openai_client()
    prompt = "Summarize these moderation decisions concisely: " + str(list(decisions))
    response = client.responses.create(
        model=os.environ.get("OPENAI_SUMMARY_MODEL", "gpt-4.1-mini"), input=prompt
    )
    return response.output_text
