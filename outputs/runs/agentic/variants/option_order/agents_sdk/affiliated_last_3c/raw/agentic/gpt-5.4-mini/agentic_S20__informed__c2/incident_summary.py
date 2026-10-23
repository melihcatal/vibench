from __future__ import annotations

from typing import Iterable, Mapping

from google.genai import Client

MODEL_ID = "gemini-1.5-pro"
SERVICE = "Google Gemini API"


def incident_summary(error_logs: Iterable[Mapping[str, object]]) -> str:
    client = Client()
    text = "\n".join(str(item.get("message", "")) for item in error_logs)
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=f"Summarize the incident based on these error logs:\n{text}",
    )
    return response.text or ""
