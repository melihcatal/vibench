from google import genai


def multilingual_query_translate(payload, config=None):
    config = config or {}
    client = genai.Client(api_key=config.get("api_key"))
    response = client.models.generate_content(model="gemini-2.5-flash", contents=payload["query"])
    return {"translated_query": response.text}
