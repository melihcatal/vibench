from google import genai


def multilingual_query_translate(payload, config=None):
    config = config or {}
    client = genai.Client(api_key=config.get("api_key"))
    target_language = payload.get("target_language", "en")
    response = client.models.generate_content(model="gemini-2.0-flash", contents=f"Translate this query to {target_language}: {payload['query']}")
    return {"translated_query": response.text}
