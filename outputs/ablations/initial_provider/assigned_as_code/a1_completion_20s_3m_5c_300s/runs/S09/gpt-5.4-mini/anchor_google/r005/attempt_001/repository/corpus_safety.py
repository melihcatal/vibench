from google import genai


def corpus_safety(payload, config=None):
    config = config or {}
    with genai.Client(api_key=config.get("api_key") or __import__("os").environ["GOOGLE_API_KEY"]) as client:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=payload["text"])
    return {"safe": "unsafe" not in response.text.lower(), "analysis": response.text}
