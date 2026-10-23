from typing import Any, Dict

from openai import OpenAI

from safety_client import get_openai_client


def appeal_translate(text: str, target_language: str) -> Dict[str, Any]:
    client = get_openai_client()
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": f"Translate moderation appeal text into {target_language} while preserving legal and review terminology. Return JSON with translated_text.",
            },
            {"role": "user", "content": text},
        ],
        text={"format": {"type": "json_object"}},
    )
    return {"translated_text": response.output_text}
