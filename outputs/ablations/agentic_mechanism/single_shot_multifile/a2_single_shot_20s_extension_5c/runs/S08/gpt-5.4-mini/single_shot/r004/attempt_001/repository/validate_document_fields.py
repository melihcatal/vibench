from typing import Any, Dict, List
from document_client import get_openai_client, get_validation_model
from document_models import ValidationResult, parse_validation_result

MODEL_ID = get_validation_model()


def validate_document_fields(document_data: Dict[str, Any], required_fields: List[str] | None = None) -> ValidationResult:
    client = get_openai_client()
    required_fields = required_fields or ["vendor", "date", "total"]
    prompt = (
        "Validate that the document JSON contains required structured fields and confidence scores. "
        f"Required fields: {required_fields}. Return JSON with keys valid, missing_fields, low_confidence_fields, score.\n\n"
        f"Document JSON:\n{document_data}"
    )
    response = client.responses.create(
        model=MODEL_ID,
        input=prompt,
        temperature=0,
    )
    return parse_validation_result(response.output_text)
