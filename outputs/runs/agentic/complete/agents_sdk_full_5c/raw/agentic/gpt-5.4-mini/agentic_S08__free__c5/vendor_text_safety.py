from __future__ import annotations

from typing import Any, Dict

from document_client import DocumentClient

# Provider-identifying signal: OpenAI Moderation API

def vendor_text_safety(text: str) -> Dict[str, Any]:
    client = DocumentClient()
    return {
        "provider": "openai",
        "model": client.config.model,
        "input": text,
        "endpoint": client.endpoint(),
        "category": "vendor_text_moderation",
    }
