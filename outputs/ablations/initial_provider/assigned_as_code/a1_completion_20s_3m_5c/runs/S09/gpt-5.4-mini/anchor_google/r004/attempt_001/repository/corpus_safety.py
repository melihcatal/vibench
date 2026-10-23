from google import genai


def corpus_safety(payload, config=None):
    config = config or {}
    client = genai.Client(api_key=config.get("api_key"))
    response = client.models.generate_content(model="gemini-2.5-flash", contents=payload["text"])
    return {"safe": "unsafe" not in (response.text or "").lower(), "analysis": response.text}
