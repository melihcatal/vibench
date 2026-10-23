import os

from google import genai


def invoke_platform_model(prompt: str) -> str:
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(
        model=os.environ.get("GEMINI_MODEL", "gemini-2.0-flash"),
        contents=prompt,
    )
    return response.text or ""


if __name__ == "__main__":
    raise SystemExit(invoke_platform_model(os.environ.get("PROMPT", "Hello")))
