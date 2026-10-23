from __future__ import annotations

import os
from typing import Iterable, Iterator

import google.generativeai as genai

from speech_models import normalize_transcript

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")


def translate_live_captions(captions: Iterable[str], target_language: str) -> Iterator[str]:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(GEMINI_MODEL)
    for caption in captions:
        prompt = f"Translate this live caption into {target_language} and keep it concise: {normalize_transcript(caption)}"
        response = model.generate_content(prompt)
        yield response.text.strip()
