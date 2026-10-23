import os

from google import genai


def translate_result(text: str, target_language: str) -> str:
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    response = client.models.generate_content(
        model=os.getenv("GOOGLE_GENAI_TRANSLATION_MODEL", "gemini-2.0-flash"),
        contents=f"Translate the following text to {target_language}:\n\n{text}",
        config={"temperature": 0.0, "max_output_tokens": 1024},
    )
    return getattr(response, "text", str(response))
