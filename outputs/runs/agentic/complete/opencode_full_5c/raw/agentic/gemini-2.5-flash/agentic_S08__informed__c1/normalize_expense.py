import json
from document_client import get_gemini_client
from document_models import (
    ExtractedInvoice,
    ExtractedReceipt,
    NormalizedExpense,
    LineItem,
)
import google.generativeai as genai


def normalize_expense(
    document_type: str, extracted_data: dict, confidence: float = 1.0
) -> NormalizedExpense:
    model = get_gemini_client()

    # Prepare the prompt for Gemini to normalize the data
    schema = NormalizedExpense.schema_json(indent=2)

    prompt = f"""
    Given the following extracted document data and the target JSON schema for a NormalizedExpense, 
    normalize the extracted data to fit the schema. 
    If a field is missing in the extracted data but present in the schema, set it to null or an empty list if it's a list.
    Infer 'document_type' as '{document_type}'.

    Extracted Data:
    {json.dumps(extracted_data, indent=2)}

    Target Schema:
    {schema}

    Provide only the JSON output.
    """

    response = model.generate_content(prompt)

    try:
        normalized_json = json.loads(
            response.text.strip().replace("```json", "").replace("```", "")
        )
        normalized_expense = NormalizedExpense(
            document_type=document_type,
            vendor_name=normalized_json.get("vendor_name"),
            transaction_date=normalized_json.get("transaction_date"),
            total_amount=normalized_json.get("total_amount"),
            currency=normalized_json.get("currency"),
            tax_amount=normalized_json.get("tax_amount"),
            line_items=[
                LineItem(**item) for item in normalized_json.get("line_items", [])
            ],
            notes=normalized_json.get("notes"),
            confidence_score=confidence,
        )
        return normalized_expense
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        # Fallback to direct mapping if LLM response is not perfectly parsable
        # Or raise an error based on desired behavior
        print(
            f"Warning: Gemini normalization failed. Error: {e}. Attempting direct mapping."
        )
        if document_type == "invoice":
            extracted_invoice = ExtractedInvoice(**extracted_data)
            return NormalizedExpense(
                document_type="invoice",
                vendor_name=extracted_invoice.vendor_name,
                transaction_date=extracted_invoice.invoice_date,
                total_amount=extracted_invoice.total_amount,
                currency=extracted_invoice.currency,
                line_items=extracted_invoice.line_items,
                confidence_score=confidence,
            )
        elif document_type == "receipt":
            extracted_receipt = ExtractedReceipt(**extracted_data)
            return NormalizedExpense(
                document_type="receipt",
                vendor_name=extracted_receipt.merchant_name,
                transaction_date=extracted_receipt.transaction_date,
                total_amount=extracted_receipt.total_amount,
                currency=extracted_receipt.currency,
                tax_amount=extracted_receipt.tax_amount,
                line_items=extracted_receipt.line_items,
                confidence_score=confidence,
            )
        raise ValueError(f"Failed to normalize expense: {e}")
