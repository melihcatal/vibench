from google import genai


def multilingual_query_translate(query, target_language="en", model="gemini-2.0-flash"):
    client = genai.Client()
    response = client.models.generate_content(model=model, contents=f"Translate to {target_language}: {query}")
    return getattr(response, "text", str(response))
