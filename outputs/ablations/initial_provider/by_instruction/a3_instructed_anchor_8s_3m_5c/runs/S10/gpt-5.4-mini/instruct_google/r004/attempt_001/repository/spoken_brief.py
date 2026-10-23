from google import genai


def spoken_brief(text: str) -> str:
    client = genai.Client(api_key="")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Turn this into a short spoken brief:\n\n{text}",
    )
    return getattr(response, "text", "")
