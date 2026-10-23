from typing import Dict, Any, List, Tuple
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.core.credentials import AzureKeyCredential
import os


def validate_document_fields(
    document_path: str, document_type: str = "invoice"
) -> Dict[str, Any]:
    """
    Validate required structured fields and confidence scores using Azure Document Intelligence.
    """
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Document Intelligence credentials not configured")

    client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    with open(document_path, "rb") as f:
        document_content = f.read()

    model_id = "prebuilt-invoice" if document_type == "invoice" else "prebuilt-receipt"

    poller = client.begin_analyze_document(
        model_id, AnalyzeDocumentRequest(bytes_source=document_content)
    )
    result = poller.result()

    validation_results = {
        "is_valid": False,
        "required_fields": [],
        "missing_fields": [],
        "confidence_scores": {},
        "field_validations": {},
    }

    if not result.documents:
        validation_results["is_valid"] = False
        validation_results["missing_fields"] = ["document_not_detected"]
        return validation_results

    document = result.documents[0]
    fields = document.fields

    required_fields_map = {
        "invoice": ["VendorName", "InvoiceDate", "InvoiceTotal"],
        "receipt": ["MerchantName", "Total"],
    }

    required_fields = required_fields_map.get(document_type, [])

    all_fields_present = True
    for field_name in required_fields:
        if field_name in fields:
            field = fields[field_name]
            confidence = field.confidence if hasattr(field, "confidence") else 0.0
            validation_results["confidence_scores"][field_name] = confidence
            validation_results["field_validations"][field_name] = {
                "present": True,
                "confidence": confidence,
                "value": field.value_string
                if hasattr(field, "value_string")
                else field.value_date
                if hasattr(field, "value_date")
                else field.value_number
                if hasattr(field, "value_number")
                else None,
            }

            if confidence < 0.7:
                validation_results["field_validations"][field_name]["warning"] = (
                    f"Low confidence: {confidence}"
                )
        else:
            validation_results["missing_fields"].append(field_name)
            validation_results["field_validations"][field_name] = {
                "present": False,
                "confidence": 0.0,
                "value": None,
            }
            all_fields_present = False

    validation_results["required_fields"] = required_fields
    validation_results["is_valid"] = (
        all_fields_present and len(validation_results["missing_fields"]) == 0
    )

    overall_confidence = 0.0
    if validation_results["confidence_scores"]:
        overall_confidence = sum(
            validation_results["confidence_scores"].values()
        ) / len(validation_results["confidence_scores"])

    validation_results["overall_confidence"] = overall_confidence

    return validation_results
