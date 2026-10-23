from google import genai


def result_translate(text: str, target_language: str) -> str:
    client = genai.Client(api_key="")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Translate the following text to {target_language}:\n\n{text}",
    )
    return getattr(response, "text", "")
