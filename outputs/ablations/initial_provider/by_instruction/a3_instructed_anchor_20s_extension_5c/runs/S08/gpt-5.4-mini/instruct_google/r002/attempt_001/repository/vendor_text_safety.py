from google import genai


def vendor_text_safety(text: str) -> dict:
    client = genai.Client(api_key=None)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=["Moderate this vendor memo for safety and return JSON label and rationale.", text],
    )
    return {"result": response.text}
