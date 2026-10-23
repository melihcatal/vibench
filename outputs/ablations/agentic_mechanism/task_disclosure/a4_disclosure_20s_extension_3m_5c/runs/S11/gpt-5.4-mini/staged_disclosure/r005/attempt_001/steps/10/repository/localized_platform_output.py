import os

from google import genai


def localized_platform_output(text: str, locale: str = "es") -> str:
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    prompt = (
        f"Translate the following platform model output into {locale}. "
        "Preserve meaning, formatting, and any technical terms where appropriate.\n\n"
        f"{text}"
    )
    response = client.models.generate_content(
        model=os.environ.get("GEMINI_MODEL", "gemini-2.0-flash"),
        contents=prompt,
    )
    return response.text or ""


if __name__ == "__main__":
    raise SystemExit(localized_platform_output(os.environ.get("TEXT", ""), os.environ.get("LOCALE", "es")))
