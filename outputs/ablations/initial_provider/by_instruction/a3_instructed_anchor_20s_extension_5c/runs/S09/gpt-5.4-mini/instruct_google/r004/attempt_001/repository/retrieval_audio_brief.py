from typing import Iterable, Dict

from google import genai


def retrieval_audio_brief(results: Iterable[str], api_key: str) -> Dict[str, str]:
    client = genai.Client(api_key=api_key)
    joined = "\n".join(results)
    result = client.models.generate_content(model="gemini-2.0-flash", contents=f"Create a spoken brief from these retrieved search results:\n{joined}")
    return {"brief": result.text}
