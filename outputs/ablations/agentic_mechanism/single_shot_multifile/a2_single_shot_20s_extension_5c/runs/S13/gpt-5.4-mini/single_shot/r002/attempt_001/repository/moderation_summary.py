from typing import Any, Dict, List
from openai import OpenAI
from safety_client import get_openai_client

SUMMARY_MODEL = "gpt-4.1-mini"


def moderation_summary(decisions: List[Dict[str, Any]], client: OpenAI = None) -> Dict[str, Any]:
    client = client or get_openai_client()
    prompt = "Summarize these moderation decisions for an operations reviewer: " + str(decisions)
    resp = client.responses.create(model=SUMMARY_MODEL, input=prompt)
    return {"summary": resp.output_text, "model": SUMMARY_MODEL}
