from __future__ import annotations

from typing import Any, Dict

from document_client import DocumentClient

# Provider-identifying signal: OpenAI API and gpt-4.1-mini model family

def invoice_summary(invoice_fields: Dict[str, Any]) -> Dict[str, Any]:
    client = DocumentClient()
    summary_text = f"Invoice from {invoice_fields.get('vendor', '')} totaling {invoice_fields.get('total', '')}."
    return {
        "model": client.config.model,
        "summary": summary_text,
        "provider": "openai",
    }
