import os

from google import genai


def spoken_brief(text: str) -> str:
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    response = client.models.generate_content(
        model=os.getenv("GOOGLE_GENAI_SPOKEN_BRIEF_MODEL", "gemini-2.0-flash"),
        contents=f"Rewrite the following into a short spoken brief suitable for audio delivery:\n\n{text}",
        config={"temperature": 0.4, "max_output_tokens": 256},
    )
    return getattr(response, "text", str(response))
