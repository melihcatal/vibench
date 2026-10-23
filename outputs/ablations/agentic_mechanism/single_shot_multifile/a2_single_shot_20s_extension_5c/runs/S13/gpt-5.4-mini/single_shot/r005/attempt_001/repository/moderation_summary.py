from typing import Any, Dict, Iterable, List, Optional
from openai import OpenAI
from safety_client import build_openai_client, provider_name

MODEL = "gpt-4o-mini"


def moderation_summary(decisions: Iterable[Dict[str, Any]], metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    client = build_openai_client()
    prompt = "Summarize the following moderation decisions concisely for an operations reviewer:\n" + str(list(decisions))
    response = client.responses.create(model=MODEL, input=prompt)
    text = getattr(response, "output_text", None)
    if not text:
        text = str(response)
    return {
        "provider": provider_name(),
        "operation": "moderation_summary",
        "model": MODEL,
        "summary": text,
        "metadata": metadata or {},
    }
