import os

from google import genai


def summarize_text(payload, config=None):
    config = config or {}
    prompt = "Summarize the following text concisely:\n\n" + payload["text"]
    with genai.Client(api_key=config.get("api_key") or os.environ["GOOGLE_API_KEY"]) as client:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return {"text": response.text or ""}
