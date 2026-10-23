import json
from typing import Union, List, Dict, Any
from document_client import get_openai_client
from document_models import (
    ExtractedInvoice,
    ExtractedReceipt,
    ExtractedField,
    ValidationResult,
)


def validate_document_fields(
    extracted_document: Union[ExtractedInvoice, ExtractedReceipt],
    required_fields: List[str],
    min_confidence: float = 0.7,
) -> List[ValidationResult]:
    openai_client = get_openai_client()

    extracted_data_dict = {}
    if isinstance(extracted_document, ExtractedInvoice):
        extracted_data_dict["document_type"] = "invoice"
        if extracted_document.vendor_name:
            extracted_data_dict["vendor_name"] = {
                "value": extracted_document.vendor_name.value,
                "confidence": extracted_document.vendor_name.confidence,
            }
        if extracted_document.invoice_date:
            extracted_data_dict["invoice_date"] = {
                "value": extracted_document.invoice_date.value,
                "confidence": extracted_document.invoice_date.confidence,
            }
        if extracted_document.total_amount:
            extracted_data_dict["total_amount"] = {
                "value": extracted_document.total_amount.value,
                "confidence": extracted_document.total_amount.confidence,
            }
        if extracted_document.currency:
            extracted_data_dict["currency"] = {
                "value": extracted_document.currency.value,
                "confidence": extracted_document.currency.confidence,
            }
        if extracted_document.total_tax:
            extracted_data_dict["total_tax"] = {
                "value": extracted_document.total_tax.value,
                "confidence": extracted_document.total_tax.confidence,
            }

    elif isinstance(extracted_document, ExtractedReceipt):
        extracted_data_dict["document_type"] = "receipt"
        if extracted_document.merchant_name:
            extracted_data_dict["merchant_name"] = {
                "value": extracted_document.merchant_name.value,
                "confidence": extracted_document.merchant_name.confidence,
            }
        if extracted_document.transaction_date:
            extracted_data_dict["transaction_date"] = {
                "value": extracted_document.transaction_date.value,
                "confidence": extracted_document.transaction_date.confidence,
            }
        if extracted_document.total_amount:
            extracted_data_dict["total_amount"] = {
                "value": extracted_document.total_amount.value,
                "confidence": extracted_document.total_amount.confidence,
            }
        if extracted_document.total_tax:
            extracted_data_dict["total_tax"] = {
                "value": extracted_document.total_tax.value,
                "confidence": extracted_document.total_tax.confidence,
            }
        if extracted_document.currency:
            extracted_data_dict["currency"] = {
                "value": extracted_document.currency.value,
                "confidence": extracted_document.currency.confidence,
            }

    validation_prompt = f"""Validate the following extracted document fields against the required fields and minimum confidence. \n\nRequired fields: {", ".join(required_fields)}\nMinimum confidence: {min_confidence}\n\nExtracted Data:\n{json.dumps(extracted_data_dict, indent=2)}\n\nProvide the validation results as a JSON array of objects, where each object has 'field_name' (string), 'is_valid' (boolean), 'reason' (string, if not valid), and 'confidence' (float). Only include fields that are part of the required_fields list or if their confidence is below the minimum."""

    chat_completion = openai_client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an expert at validating document extraction data based on required fields and confidence scores. Output only a JSON array.",
            },
            {"role": "user", "content": validation_prompt},
        ],
        response_format={"type": "json_object"},
    )

    validation_results_json_str = chat_completion.choices[0].message.content
    validation_data = json.loads(validation_results_json_str)

    results: List[ValidationResult] = []
    for item in validation_data:
        results.append(
            ValidationResult(
                field_name=item.get("field_name"),
                is_valid=item.get("is_valid"),
                reason=item.get("reason"),
                confidence=item.get("confidence"),
            )
        )

    # Also perform local validation for quick checks
    for field_name in required_fields:
        field_data = extracted_data_dict.get(field_name)
        if field_name not in [
            r.field_name for r in results
        ]:  # Avoid duplicate if LLM already handled it
            if field_data is None or field_data.get("value") is None:
                results.append(
                    ValidationResult(
                        field_name=field_name, is_valid=False, reason="Field is missing"
                    )
                )
            elif field_data.get("confidence", 1.0) < min_confidence:
                results.append(
                    ValidationResult(
                        field_name=field_name,
                        is_valid=False,
                        reason=f"Confidence {field_data.get('confidence'):.2f} is below minimum {min_confidence:.2f}",
                        confidence=field_data.get("confidence"),
                    )
                )
            else:
                results.append(
                    ValidationResult(
                        field_name=field_name,
                        is_valid=True,
                        confidence=field_data.get("confidence"),
                    )
                )

    return results
