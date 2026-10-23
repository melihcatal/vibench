# [LATER-STEP] document_field_extraction.py

import openai
from document_client import DocumentClient
from document_models import OCRRequest, normalize_ocr_response


def extract_fields_from_ocr(image_path: str, schema: List[dict]) -> Dict[str, str]:
    """Extract structured fields from OCR-normalized text using an LLM prompt.

    Args:
        image_path: Path to scanned image.
        schema: List of dicts describing required fields, e.g. [{\"name\":\"Date\",\"type\":\"date\"}, {\"name\":\"Amount\",\"type\":\"number\"}].

    Returns:
        Dict mapping field name to extracted value.
    """
    client = DocumentClient()
    raw_text = client.extract_text(image_path)
    lines = normalize_ocr_response(raw_text)
    full_text = "\\n".join(lines)
    prompt = (
        f"""You are given the raw OCR text of a form:
\n{text}\n\nExtract the following fields (preserve capitalization exactly as listed) and output a JSON object with key: value pairs, one per line:\n"""
        + "\\n".join([f"{field['name']}:" for field in schema])
        + "\\n"
    )
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )
    # Simple JSON parsing of response
    raw_result = response.choices[0].message.content.strip()
    import json

    try:
        result = json.loads(raw_result)
    except json.JSONDecodeError:
        result = {}
    return result
