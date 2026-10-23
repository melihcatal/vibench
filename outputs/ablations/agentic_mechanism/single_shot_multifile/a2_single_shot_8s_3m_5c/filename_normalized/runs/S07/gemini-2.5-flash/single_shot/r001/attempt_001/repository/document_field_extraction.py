import json
from document_client import get_text_generation_model
from document_models import ExtractedField, DocumentFieldsExtractionResult

def extract_structured_fields(document_text: str, extraction_schema: dict) -> DocumentFieldsExtractionResult:
    model = get_text_generation_model(model_name="gemini-pro")
    schema_str = json.dumps(extraction_schema)
    prompt = f"""Extract information from the following document text according to the provided JSON schema.
Return the extracted information as a JSON object matching the schema. If a field is not found, use null.

Document Text:
---
{document_text}
---

JSON Schema:
{schema_str}

Extracted JSON:
"""
    response = model.predict(prompt)
    extracted_json_str = response.text.strip()
    fields: list[ExtractedField] = []
    try:
        extracted_data = json.loads(extracted_json_str)
        for field_name, field_value in extracted_data.items():
            if field_name in extraction_schema:
                fields.append(ExtractedField(
                    field_name=field_name,
                    field_value=str(field_value) if field_value is not None else "",
                    confidence=None,
                    source_text_segments=[]
                ))
    except json.JSONDecodeError:
        pass
    return DocumentFieldsExtractionResult(
        fields=fields,
        raw_response=response._prediction_response.to_dict() if hasattr(response, '_prediction_response') else {}
    )