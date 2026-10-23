import json


def build_extraction_payload(document_text, schema, confidence_threshold):
    return json.dumps({"document_text": document_text, "schema": schema, "confidence_threshold": confidence_threshold})


def build_normalization_payload(extracted_fields):
    return json.dumps({"extracted_fields": extracted_fields, "target_schema": {"merchant": "string", "total": "number", "currency": "string", "category": "string", "date": "string", "items": "array"}})


def build_validation_payload(document_fields):
    return json.dumps({"document_fields": document_fields, "required_fields": ["vendor", "date", "total"], "confidence_fields": ["vendor_confidence", "date_confidence", "total_confidence"]})


def coerce_json_response(response):
    return json.loads(response.output_text)


def coerce_extraction_response(response):
    return coerce_json_response(response)
