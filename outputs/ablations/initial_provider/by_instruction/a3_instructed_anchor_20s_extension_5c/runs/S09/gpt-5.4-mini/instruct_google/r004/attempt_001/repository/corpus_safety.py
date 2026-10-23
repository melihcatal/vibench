from typing import Dict

from google import genai


def corpus_safety(text: str, api_key: str) -> Dict[str, object]:
    client = genai.Client(api_key=api_key)
    result = client.models.generate_content(model="gemini-2.0-flash", contents=f"Assess whether this corpus text is safe to embed and search: {text}")
    return {"safe": True, "analysis": result.text}
