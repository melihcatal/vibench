from typing import Dict, List, Optional
import re
from pydantic import BaseModel
from document_models import OCRResponse


class FieldExtractionResult(BaseModel):
    field_name: str
    value: str
    confidence: float


def document_field_extraction(
    ocr_response: OCRResponse,
) -> Dict[str, List[FieldExtractionResult]]:
    """Extract structured fields from OCR-normalized document text using regex patterns."""
    text = ocr_response.text

    # Example patterns for common fields
    patterns = {
        "invoice_number": r"invoice\s*(?:no|number|#)?\s*[:\-\s]?\s*([a-zA-Z0-9\-]+)",
        "date": r"date\s*[:\-\s]?\s*([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})",
        "total_amount": r"total\s*(?:amount|due)?\s*[:\-\s]?\s*\$?([0-9]+\.[0-9]{2})",
        "vendor_name": r"(?:vendor|supplier|from)\s*[:\-\s]?\s*([a-zA-Z\s&]+)",
        "customer_name": r"(?:customer|bill to|to)\s*[:\-\s]?\s*([a-zA-Z\s]+)",
    }

    results = {}
    for field_name, pattern in patterns.items():
        matches = re.finditer(pattern, text, re.IGNORECASE)
        field_results = []
        for match in matches:
            field_results.append(
                FieldExtractionResult(
                    field_name=field_name,
                    value=match.group(1).strip(),
                    confidence=0.9,  # Simplified confidence for regex-based extraction
                )
            )
        results[field_name] = field_results

    return {"provider": "regex_based_extraction", "fields": results}
