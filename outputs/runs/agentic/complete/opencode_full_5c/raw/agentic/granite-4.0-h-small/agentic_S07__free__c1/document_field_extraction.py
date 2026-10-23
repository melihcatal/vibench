# [LATER-STEP] document_field_extraction.py
"""Extract structured fields from normalized OCR text using regexes / simple rules"""

import re
from typing import Dict, Any, List
from document_models import OCRResponse, KeyValueResponse

# Example field definitions (these could be loaded from a config file)
FIELD_RULES = {
    "date": r"(?i)\b(?:date|issued on)\s*[:=]\s*(\d{1,2}/\d{1,2}/\d{2,4})\b",
    "invoice_number": r"(?i)\\b(?:invoice|inv)\\s*[:=]\\s*(\w+)\\b",
    "total_amount": r"\\btotal\\s*[:=]\\s*[$]?(\d+(?:,\\d{3})*\\.\\d{2})\\b",
    "vendor_name": r"(?i)vendor\\s*[:=]\\s*([A-Za-z ]+)",
}


def extract_fields(response: OCRResponse) -> Dict[str, Any]:
    """Simple rule‑based field extraction from OCR blocks"""
    text = response.text.lower()
    fields = {}
    for name, pattern in FIELD_RULES.items():
        match = re.search(pattern, text)
        if match:
            fields[name] = match.group(1)
    return fields


# Alternative rule based on KeyValueResponse (if using Textract FORMS)
def extract_fields_from_keyvalues(kv_resp: KeyValueResponse) -> Dict[str, Any]:
    fields = {}
    for entry in kv_resp.key_values:
        # KeyValue blocks have a KEY and a VALUE child
        if entry.get("Type") == "KEY":
            key_text = entry.get("Text", "")
            # Find the associated VALUE block (simple heuristic: next block is VALUE)
            value_text = None
            for blk in kv_resp.raw.get("Blocks", []):
                if blk.get("ParentId").get("Id"):  # placeholder heuristic
                    value_text = blk.get("Text", "")
                    break
            if value_text:
                fields[key_text] = value_text
    return fields


if __name__ == "__main__":
    import json, sys

    if len(sys.argv) != 2:
        print("Usage: python document_field_extraction.py <ocr-json>")
        sys.exit(1)
    with open(sys.argv[1], "r") as f:
        ocr_json = json.load(f)
    ocr_resp = OCRResponse(ocr_json)
    print("Extracted fields:", extract_fields(ocr_resp))
