from typing import Any, Dict

import openai


def summarize_invoice_fields(extracted: Dict[str, Any]) -> Dict[str, Any]:
    client = openai.OpenAI()
    text = f"Summarize invoice from {extracted.get('vendor', {}).get('value', '')} totaling {extracted.get('total', {}).get('value', '')}."
    return {"provider": "openai", "model": "gpt-5.4-mini", "summary": text, "client": str(type(client).__name__)}
