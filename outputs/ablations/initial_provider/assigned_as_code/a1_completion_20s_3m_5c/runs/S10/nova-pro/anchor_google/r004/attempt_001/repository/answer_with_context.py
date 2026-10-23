import os

from google import genai


def answer_with_context(payload, config=None):
    config = config or {}
    prompt = "Answer the following question using the provided context:

Question: " + payload["question"] + "\nContext: " + payload["context"]
    with genai.Client(api_key=config.get("api_key") or os.environ["GOOGLE_API_KEY"]) as client:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return {"text": response.text or ""}