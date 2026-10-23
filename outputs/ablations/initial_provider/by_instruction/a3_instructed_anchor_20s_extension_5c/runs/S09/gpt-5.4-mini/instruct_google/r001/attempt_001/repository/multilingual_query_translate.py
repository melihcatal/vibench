from google import genai


def multilingual_query_translate(query, target_language="en"):
    client = genai.Client(api_key="")
    prompt = f"Translate the query to {target_language}: {query}"
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    return response.text
