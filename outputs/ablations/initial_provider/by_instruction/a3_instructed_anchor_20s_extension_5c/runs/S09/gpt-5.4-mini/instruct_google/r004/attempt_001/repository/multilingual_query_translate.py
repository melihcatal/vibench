from typing import Dict

from google import genai


def multilingual_query_translate(query: str, target_language: str, api_key: str) -> Dict[str, str]:
    client = genai.Client(api_key=api_key)
    result = client.models.generate_content(model="gemini-2.0-flash", contents=f"Translate this query to {target_language}: {query}")
    return {"translated_query": result.text, "target_language": target_language}
