from google import genai


def invoice_note_translate(text: str, target_language: str) -> str:
    client = genai.Client(api_key=None)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[f"Translate this invoice note into {target_language}.", text],
    )
    return response.text
