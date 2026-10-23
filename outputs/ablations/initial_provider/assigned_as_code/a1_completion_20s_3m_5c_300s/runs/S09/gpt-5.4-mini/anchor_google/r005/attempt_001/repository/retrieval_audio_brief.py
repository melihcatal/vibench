from google import genai


def retrieval_audio_brief(payload, config=None):
    config = config or {}
    summary = " ".join(item["text"] for item in payload["results"])
    with genai.Client(api_key=config.get("api_key") or __import__("os").environ["GOOGLE_API_KEY"]) as client:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=f"Create a spoken brief from these search results: {summary}")
    return {"brief": response.text}
