from typing import Any, Dict, List

from openai import OpenAI

from speech_client import get_client


def translate_transcript(
    segments: List[Dict[str, Any]], target_language: str = "en"
) -> Dict[str, Any]:
    client: OpenAI = get_client()
    text = "\n".join(segment.get("text", "") for segment in segments)
    result = client.responses.create(
        model="gpt-4.1-mini",
        input=f"Translate the following transcript to {target_language}:\n{text}",
    )
    return {"translation": result.output_text, "target_language": target_language}
