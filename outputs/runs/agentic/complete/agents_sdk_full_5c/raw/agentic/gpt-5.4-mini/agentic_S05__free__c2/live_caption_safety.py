from __future__ import annotations

import os
from typing import Iterable, Iterator

import google.generativeai as genai

SAFETY_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")


def check_live_caption_safety(captions: Iterable[str]) -> Iterator[bool]:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(SAFETY_MODEL)
    for caption in captions:
        prompt = f"Classify whether this live transcript contains unsafe content. Answer only SAFE or UNSAFE: {caption}"
        response = model.generate_content(prompt)
        yield response.text.strip().upper().startswith("SAFE")
