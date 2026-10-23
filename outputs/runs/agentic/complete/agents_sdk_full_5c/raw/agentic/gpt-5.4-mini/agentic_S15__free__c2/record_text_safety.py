from __future__ import annotations

from typing import Any, Dict, List

from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

from database_models import as_iso_utc


def check_text_safety(text_fields: List[str]) -> Dict[str, Any]:
    endpoint = __import__("os").environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = __import__("os").environ["AZURE_CONTENT_SAFETY_KEY"]
    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    joined = "\n".join(text_fields)
    result = client.analyze_text({"text": joined})
    return {
        "provider": "azure-ai-contentsafety",
        "generated_at": as_iso_utc(),
        "result": getattr(result, "as_dict", lambda: {"status": "ok"})(),
    }
