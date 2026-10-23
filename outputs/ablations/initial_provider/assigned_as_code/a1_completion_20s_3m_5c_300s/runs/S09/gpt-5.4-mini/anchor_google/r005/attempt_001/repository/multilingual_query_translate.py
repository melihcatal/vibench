from google import genai


def multilingual_query_translate(payload, config=None):
    config = config or {}
    target_language = payload.get("target_language", "English")
    with genai.Client(api_key=config.get("api_key") or __import__("os").environ["GOOGLE_API_KEY"]) as client:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=f"Translate this query to {target_language}: {payload['query']}")
    return {"translated_query": response.text}
