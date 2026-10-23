from google import genai


def prompt_safety(text: str) -> str:
    client = genai.Client(api_key="")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Assess safety of this text and return a brief label:\n\n{text}",
    )
    return getattr(response, "text", "")
