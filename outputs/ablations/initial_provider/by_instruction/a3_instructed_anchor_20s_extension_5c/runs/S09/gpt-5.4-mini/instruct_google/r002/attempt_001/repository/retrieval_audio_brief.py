import os

import google.generativeai as genai


def retrieval_audio_brief(results: list[str]) -> str:
    model = os.getenv("GOOGLE_AUDIO_BRIEF_MODEL", "gemini-1.5-flash")
    prompt = "Create a concise spoken brief from these retrieval results: " + " | ".join(results)
    response = genai.GenerativeModel(model).generate_content(prompt)
    return response.text
