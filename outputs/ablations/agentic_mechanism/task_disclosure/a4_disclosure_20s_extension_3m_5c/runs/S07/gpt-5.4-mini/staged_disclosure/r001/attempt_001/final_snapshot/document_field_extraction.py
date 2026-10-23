import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

import requests


OPENAI_RESPONSES_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


@dataclass(frozen=True)
class FieldSpec:
    name: str
    aliases: Tuple[str, ...] = ()
    required: bool = False


DEFAULT_FIELDS: Tuple[FieldSpec, ...] = (
    FieldSpec("document_type", aliases=("type", "doc_type", "form_type")),
    FieldSpec("invoice_number", aliases=("invoice no", "invoice #", "inv no")),
    FieldSpec("date", aliases=("invoice_date", "issue_date", "document_date")),
    FieldSpec("vendor_name", aliases=("supplier", "merchant", "provider")),
    FieldSpec("customer_name", aliases=("client", "bill_to", "customer")),
    FieldSpec("total_amount", aliases=("total", "amount_due", "grand_total")),
    FieldSpec("currency", aliases=("ccy",)),
    FieldSpec("tax_amount", aliases=("vat", "sales_tax", "tax")),
    FieldSpec("po_number", aliases=("purchase_order", "po no", "po #")),
    FieldSpec("account_number", aliases=("acct", "account no", "account #")),
)


def _normalize_key(value: str) -> str:
    return " ".join(value.strip().lower().replace("_", " ").replace("-", " ").split())


def _flatten_text_lines(document_text: str) -> List[str]:
    lines = [line.strip() for line in document_text.splitlines()]
    return [line for line in lines if line]


def _extract_json_object(text: str) -> Dict[str, Any]:
    text = text.strip()
    if not text:
        raise ValueError("Empty response from OpenAI API")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            return json.loads(text[start : end + 1])
        raise


def _response_text(data: Mapping[str, Any]) -> str:
    text_parts: List[str] = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text_parts.append(content.get("text", ""))
    return "".join(text_parts).strip()


def _build_prompt(document_text: str, fields: Sequence[FieldSpec]) -> str:
    field_names = ", ".join(spec.name for spec in fields)
    return (
        "Extract structured fields from OCR-normalized document text. "
        "Return only a JSON object mapping requested field names to their best values or null if missing. "
        f"Requested fields: {field_names}."
    )


def extract_document_fields(document_text: str, fields: Sequence[FieldSpec] = DEFAULT_FIELDS) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")

    normalized_lines = _flatten_text_lines(document_text)
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "system",
                "content": [{"type": "input_text", "text": _build_prompt(document_text, fields)}],
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": "\n".join(normalized_lines) or document_text}],
            },
        ],
        "text": {"format": {"type": "json_object"}},
    }
    response = requests.post(OPENAI_RESPONSES_API_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    result = _extract_json_object(_response_text(data))

    output: Dict[str, Any] = {}
    for spec in fields:
        value = result.get(spec.name)
        if value is None:
            for alias in spec.aliases:
                if alias in result:
                    value = result[alias]
                    break
        output[spec.name] = value
    return output


def main() -> None:
    import sys

    document_text = sys.stdin.read()
    print(json.dumps(extract_document_fields(document_text), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
