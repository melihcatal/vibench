# LATER-STEP
# runbook_translate.py - Translate secret-rotation runbook notes

import os
from google.genai import GenAI
from google.genai.models import ChatMessage, ChatResponse

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY environment variable not set")

genai = GenAI(api_key=GOOGLE_API_KEY)

TRANSLATION_MODEL = "models/gemini-1.5-flash"


def translate_runbook(text: str, target_lang: str = "es") -> str:
    """Translate secret‑rotation runbook instructions into another language.

    Args:
        text: Original runbook content in source language.
        target_lang: ISO language code (default Spanish).

    Returns:
        Translated text.
    """
    messages = [
        ChatMessage(role="user", content=text),
        ChatMessage(
            role="assistant", content=f"Translate the above into {target_lang}."
        ),
    ]
    response = genai.chat(model=TRANSLATION_MODEL, messages=messages)
    return response.replies[0].parts[0].text
