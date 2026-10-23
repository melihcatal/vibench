import json
import os
from typing import Any, Dict, Optional

from openai import OpenAI


class DocumentFieldExtractionError(Exception):
    pass


def extract_fields(text: str, model: str = "gpt-5.4-mini") -> Dict[str, Any]:
    if not text or not text.strip():
        raise DocumentFieldExtractionError("text is required")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": (
                    "Extract structured fields from OCR-normalized document text and return "
                    "valid JSON only. Include keys when inferable: document_type, "
                    "document_number, issue_date, due_date, total_amount, currency, "
                    "vendor_name, customer_name, tax_amount, line_items, and any other "
                    "salient fields with confidence-aware normalization."
                ),
            },
            {"role": "user", "content": text},
        ],
    )

    output_text = getattr(response, "output_text", None)
    if not output_text:
        try:
            output_text = response.output[0].content[0].text  # type: ignore[index]
        except Exception as exc:
            raise DocumentFieldExtractionError("empty model response") from exc

    try:
        return json.loads(output_text)
    except json.JSONDecodeError as exc:
        raise DocumentFieldExtractionError("model did not return valid JSON") from exc


def extract_fields_from_file(path: str, encoding: str = "utf-8") -> Dict[str, Any]:
    with open(path, "r", encoding=encoding) as f:
        return extract_fields(f.read())


def main(argv: Optional[list[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Extract structured fields from OCR-normalized document text")
    parser.add_argument("path", help="Path to OCR-normalized text file")
    parser.add_argument("--model", default="gpt-5.4-mini")
    args = parser.parse_args(argv)

    result = extract_fields_from_file(args.path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
