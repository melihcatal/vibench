from __future__ import annotations

from google import genai


MODEL_ID = "gemini-2.0-flash"


def translate_consent_copy(text: str, target_language: str) -> str:
    client = genai.Client()
    resp = client.models.generate_content(
        model=MODEL_ID,
        contents=f"Translate this identity-provider consent copy into {target_language}, preserving legal meaning:\n{text}",
    )
    return getattr(resp, "text", "") or ""
