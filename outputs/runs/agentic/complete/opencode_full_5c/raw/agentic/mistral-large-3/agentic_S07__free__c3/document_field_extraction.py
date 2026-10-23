from typing import Dict, List, Optional
import re
from document_models import OCRResponse


def extract_field(
    text: str, field_patterns: Dict[str, List[str]]
) -> Dict[str, Optional[str]]:
    """Extract structured fields from OCR-normalized document text using regex patterns."""
    extracted_fields = {}

    for field_name, patterns in field_patterns.items():
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                extracted_fields[field_name] = match.group(1).strip()
                break
        else:
            extracted_fields[field_name] = None

    return extracted_fields


def document_field_extraction(ocr_response: OCRResponse) -> Dict[str, Dict]:
    """Extract structured fields from OCR-normalized document text."""
    common_field_patterns = {
        "invoice_number": [
            r"invoice\s*(?:no|number)?\s*[:#]?\s*([A-Z0-9-]+)",
            r"inv\s*[:#]?\s*([A-Z0-9-]+)",
        ],
        "date": [
            r"date\s*[:#]?\s*([0-9]{1,2}[/-][0-9]{1,2}[/-][0-9]{2,4})",
            r"([0-9]{4}[/-][0-9]{1,2}[/-][0-9]{1,2})",
        ],
        "total_amount": [
            r"total\s*(?:amount)?\s*[:#]?\s*\$?([0-9,.]+)",
            r"amount\s*due\s*[:#]?\s*\$?([0-9,.]+)",
        ],
        "vendor_name": [
            r"vendor\s*[:#]?\s*([A-Za-z\s&]+)",
            r"from\s*[:#]?\s*([A-Za-z\s&]+)",
        ],
        "customer_name": [
            r"customer\s*[:#]?\s*([A-Za-z\s&]+)",
            r"bill\s*to\s*[:#]?\s*([A-Za-z\s&]+)",
        ],
    }

    extracted_fields = extract_field(ocr_response.full_text, common_field_patterns)

    return {
        "fields": extracted_fields,
        "provider": "regex_based",
        "model": "pattern_matching",
    }
