from __future__ import annotations

from collections.abc import Sequence

from google import genai


SAFETY_MODEL = "gemini-2.0-flash"


def corpus_safety(texts: Sequence[str]) -> dict:
    client = genai.Client()
    joined = "\n\n---\n\n".join(texts)
    response = client.models.generate_content(
        model=SAFETY_MODEL,
        contents=(
            "Review the following corpus before it is sent to an embedding system. "
            "Identify safety risks, privacy concerns, and whether embedding should proceed. "
            "Respond with a brief decision and key issues.\n\n"
            + joined
        ),
    )
    return {
        "provider": "google_gemini",
        "model": SAFETY_MODEL,
        "assessment": response.text,
        "document_count": len(texts),
    }
