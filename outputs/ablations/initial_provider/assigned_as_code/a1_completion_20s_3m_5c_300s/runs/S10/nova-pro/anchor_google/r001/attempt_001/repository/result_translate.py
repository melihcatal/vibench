import os

from google import genai


def translate_result(payload, config=None):
    config = config or {}
    prompt = "Translate the following text to the target language:

" + payload["text"] + "\n\nTarget language: " + payload["target_language"]
    with genai.Client(api_key=config.get("api_key") or os.environ["GOOGLE_API_KEY"]) as client:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return {"text": response.text or ""}
