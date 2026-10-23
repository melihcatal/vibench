from typing import Any, Dict

from openai import OpenAI


def translate_record(record: Dict[str, Any], target_language: str) -> Dict[str, Any]:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate user-facing fields to {target_language}: {record}",
    )
    return {"translated_text": response.output_text}


def handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    return translate_record(event["record"], event["target_language"])
