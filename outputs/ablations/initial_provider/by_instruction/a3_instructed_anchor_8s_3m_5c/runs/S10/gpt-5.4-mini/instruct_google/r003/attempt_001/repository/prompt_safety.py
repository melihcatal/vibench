import os

from google import genai


def check_prompt_safety(text: str) -> str:
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    response = client.models.generate_content(
        model=os.getenv("GOOGLE_GENAI_SAFETY_MODEL", "gemini-2.0-flash"),
        contents=f"Assess whether the following content is unsafe and explain briefly:\n\n{text}",
        config={"temperature": 0.0, "max_output_tokens": 256},
    )
    return getattr(response, "text", str(response))
