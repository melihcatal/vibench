from typing import Any, Dict, List

from openai import OpenAI

from messaging_models import ProcessingSummary


def summarize_messages(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    client = OpenAI()
    summary = client.responses.create(model="gpt-5.4-mini", input=str(records))
    return {"summary": summary.output_text, "count": len(records)}
