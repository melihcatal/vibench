from typing import Any, Dict, List

from openai import OpenAI


def translate_transcript(segments: List[Dict[str, Any]], target_language: str = "es") -> Dict[str, Any]:
    client = OpenAI()
    text = "
".join(segment.get("text", "") for segment in segments)
    prompt = f"Translate the following transcript to {target_language} and preserve line breaks:
{text}"
    result = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return {"translated_text": result.choices[0].message.content, "model": "gpt-4o-mini"}
