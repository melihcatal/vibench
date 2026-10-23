from typing import Any, Dict, List

from openai import OpenAI


def summarize_record(record: Dict[str, Any]) -> Dict[str, Any]:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Summarize this document record in one concise sentence: {record}",
    )
    return {"summary": response.output_text}


def handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    return summarize_record(event["record"])
