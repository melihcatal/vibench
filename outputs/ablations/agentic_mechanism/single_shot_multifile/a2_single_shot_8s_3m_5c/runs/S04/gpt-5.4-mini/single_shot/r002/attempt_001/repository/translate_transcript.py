from typing import Any, Dict, List

from openai import OpenAI

from speech_client import get_openai_client


def translate_transcript(segments: List[Dict[str, Any]], target_language: str = "en") -> Dict[str, Any]:
    client = get_openai_client()
    content = "\n".join(segment.get("text", "") for segment in segments)
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": f"Translate transcript text to {target_language}. Return concise translated text."},
            {"role": "user", "content": content},
        ],
    )
    return {"translation": response.output_text, "provider": "openai", "model": "gpt-4.1-mini"}
