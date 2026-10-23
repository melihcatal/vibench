import os
from typing import Dict, Any, List, Tuple
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def validate_document_fields(
    extracted_data: Dict[str, Any], document_type: str
) -> Dict[str, Any]:
    required_fields = get_required_fields(document_type)

    validation_results = {
        "is_valid": True,
        "missing_fields": [],
        "low_confidence_fields": [],
        "field_validations": {},
    }

    for field_name, field_config in required_fields.items():
        field_value = extracted_data.get(field_name)
        field_confidence = extracted_data.get("confidence")

        if field_value is None:
            validation_results["missing_fields"].append(field_name)
            validation_results["is_valid"] = False
            validation_results["field_validations"][field_name] = {
                "present": False,
                "confidence": None,
                "valid": False,
            }
        else:
            confidence_valid = True
            if field_confidence is not None and field_confidence < field_config.get(
                "min_confidence", 0.7
            ):
                validation_results["low_confidence_fields"].append(field_name)
                confidence_valid = False

            validation_results["field_validations"][field_name] = {
                "present": True,
                "confidence": field_confidence,
                "valid": confidence_valid,
            }

            if not confidence_valid:
                validation_results["is_valid"] = False

    if "confidence" in extracted_data and extracted_data["confidence"] < 0.5:
        validation_results["overall_confidence_low"] = True
        validation_results["is_valid"] = False

    return validation_results


def get_required_fields(document_type: str) -> Dict[str, Dict[str, Any]]:
    field_configs = {
        "invoice": {
            "vendor": {"min_confidence": 0.8, "required": True},
            "date": {"min_confidence": 0.7, "required": True},
            "total": {"min_confidence": 0.9, "required": True},
            "line_items": {"min_confidence": 0.6, "required": False},
        },
        "receipt": {
            "merchant": {"min_confidence": 0.8, "required": True},
            "total": {"min_confidence": 0.9, "required": True},
            "tax": {"min_confidence": 0.7, "required": False},
            "items": {"min_confidence": 0.6, "required": False},
        },
    }

    return field_configs.get(document_type, {})


def validate_with_azure_document_intelligence(
    image_path: str, document_type: str
) -> Dict[str, Any]:
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Document Intelligence credentials not configured")

    client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    model_id = "prebuilt-invoice" if document_type == "invoice" else "prebuilt-receipt"

    with open(image_path, "rb") as f:
        poller = client.begin_analyze_document(
            model_id, analyze_request=f, content_type="application/octet-stream"
        )

    result = poller.result()

    validation = {
        "document_type": document_type,
        "overall_confidence": result.documents[0].confidence
        if hasattr(result.documents[0], "confidence")
        else None,
        "fields": {},
        "is_valid": True,
    }

    required_fields = get_required_fields(document_type)

    for field_name in required_fields:
        if hasattr(result.documents[0].fields, field_name):
            field = getattr(result.documents[0].fields, field_name, None)
            if field:
                validation["fields"][field_name] = {
                    "present": True,
                    "confidence": field.confidence
                    if hasattr(field, "confidence")
                    else None,
                    "value": field.value_string
                    or field.value_number
                    or field.value_date,
                }
            else:
                validation["fields"][field_name] = {"present": False}
                validation["is_valid"] = False
        else:
            validation["fields"][field_name] = {"present": False}
            validation["is_valid"] = False

    return validation
