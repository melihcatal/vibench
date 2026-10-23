from __future__ import annotations

from typing import Any, Dict

from document_client import DocumentClient

# Provider-identifying signal: OpenAI API

def invoice_note_translate(text: str, target_language: str = "en") -> Dict[str, Any]:
    client = DocumentClient()
    return {
        "provider": "openai",
        "model": client.config.model,
        "source_language": "auto",
        "target_language": target_language,
        "text": text,
        "endpoint": client.endpoint(),
    }
