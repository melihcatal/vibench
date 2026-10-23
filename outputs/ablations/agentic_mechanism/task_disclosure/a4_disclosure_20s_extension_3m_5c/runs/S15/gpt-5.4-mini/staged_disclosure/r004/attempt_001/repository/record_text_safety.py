import json
import os
from typing import Any, Dict, Iterable, List, Optional

from openai import OpenAI


MODEL_ID = "openai/gpt-5.4-mini"


def _extract_text_fields(record: Dict[str, Any]) -> Dict[str, str]:
    text_fields: Dict[str, str] = {}
    for key, value in record.items():
        if isinstance(value, str):
            text_fields[key] = value
    return text_fields


def _safety_prompt(field_name: str, field_value: str) -> str:
    return (
        "Determine whether the following user-generated document field contains unsafe content. "
        "Unsafe content includes sexual content involving minors, explicit violence, self-harm instructions, "
        "credible threats, extremist praise or recruitment, illegal wrongdoing instructions, or malware. "
        "Return strict JSON with keys unsafe (boolean), category (string), and rationale (string).\n\n"
        f"Field: {field_name}\n"
        f"Content: {field_value}"
    )


def check_record_text_safety(record: Dict[str, Any], model: str = MODEL_ID) -> Dict[str, Dict[str, Any]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    results: Dict[str, Dict[str, Any]] = {}
    for field_name, field_value in _extract_text_fields(record).items():
        response = client.responses.create(
            model=model,
            input=_safety_prompt(field_name, field_value),
        )
        output_text = getattr(response, "output_text", None)
        if output_text is None:
            output_text = ""
            for item in getattr(response, "output", []) or []:
                for content in getattr(item, "content", []) or []:
                    text = getattr(content, "text", None)
                    if text:
                        output_text += text
        try:
            parsed = json.loads(output_text)
        except json.JSONDecodeError:
            parsed = {"unsafe": False, "category": "unknown", "rationale": output_text.strip()}
        results[field_name] = parsed
    return results


def record_text_safety(record: Dict[str, Any]) -> Dict[str, Any]:
    findings = check_record_text_safety(record)
    unsafe_fields: List[str] = [name for name, result in findings.items() if result.get("unsafe")]
    return {"unsafe_fields": unsafe_fields, "field_results": findings}
