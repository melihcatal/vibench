from __future__ import annotations

from typing import Any, Dict

from google.genai import Client

from database_models import SummaryResponse

MODEL_ID = "gemini-2.0-flash"


def summarize_record(record: Dict[str, Any]) -> SummaryResponse:
    client = Client()
    text = "\n".join(f"{k}: {v}" for k, v in record.items())
    response = client.models.generate_content(model=MODEL_ID, contents=f"Summarize this document record concisely:\n{text}")
    summary_text = getattr(response, "text", "") or str(response)
    title = str(record.get("title") or record.get("name") or "record")
    return SummaryResponse(title=title, summary=summary_text, metadata={"model": MODEL_ID})
