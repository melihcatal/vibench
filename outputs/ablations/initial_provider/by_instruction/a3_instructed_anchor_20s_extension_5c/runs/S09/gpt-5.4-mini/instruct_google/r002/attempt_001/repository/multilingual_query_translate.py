import os

import google.generativeai as genai


def multilingual_query_translate(query: str, target_language: str = "en") -> str:
    model = os.getenv("GOOGLE_TRANSLATION_MODEL", "gemini-1.5-flash")
    prompt = f"Translate the following query to {target_language}: {query}"
    response = genai.GenerativeModel(model).generate_content(prompt)
    return response.text.strip()
