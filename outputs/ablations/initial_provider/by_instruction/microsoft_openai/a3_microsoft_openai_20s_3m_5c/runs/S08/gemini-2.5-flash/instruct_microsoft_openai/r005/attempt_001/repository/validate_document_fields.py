import json
from typing import Union, List
from document_client import get_openai_client, call_openai_chat_model
from document_models import InvoiceFields, ReceiptFields, ValidationResult

def validate_document_fields(document_data: Union[InvoiceFields, ReceiptFields], model_deployment_name: str = "gpt-4o") -> List[ValidationResult]:
    """
    Validates required structured fields and confidence scores using Azure OpenAI for content-based validation.
    """
    validation_results: List[ValidationResult] = []
    client = get_openai_client()

    # Fields to validate based on document type
    if isinstance(document_data, InvoiceFields):
        fields_to_check = {
            "vendor_name": document_data.vendor_name,
            "invoice_date": document_data.invoice_date,
            "total_amount": document_data.total_amount,
        }
        document_type = "invoice"
    elif isinstance(document_data, ReceiptFields):
        fields_to_check = {
            "merchant_name": document_data.merchant_name,
            "transaction_date": document_data.transaction_date,
            "total_amount": document_data.total_amount,
        }
        document_type = "receipt"
    else:
        raise ValueError("document_data must be either InvoiceFields or ReceiptFields.")

    for field_name, value in fields_to_check.items():
        is_present = value is not None
        validation_results.append(ValidationResult(
            field_name=field_name,
            is_valid=is_present, # Basic validity: presence
            confidence=1.0 if is_present else 0.0,
            message=None if is_present else f"{field_name} is missing."
        ))

    # Use OpenAI to perform more nuanced validation (e.g., date format, amount sanity)
    # Construct a prompt for the model to validate specific fields.
    # The model will return a JSON object with validation status for selected fields.
    validation_prompt_parts = []
    if document_type == "invoice":
        if document_data.invoice_date:
            validation_prompt_parts.append(f"Is '{document_data.invoice_date}' a valid date in YYYY-MM-DD format?")
        if document_data.total_amount is not None:
            validation_prompt_parts.append(f"Is {document_data.total_amount} a reasonable total amount for an invoice (i.e., positive number)?")
    elif document_type == "receipt":
        if document_data.transaction_date:
            validation_prompt_parts.append(f"Is '{document_data.transaction_date}' a valid date in YYYY-MM-DD format?")
        if document_data.total_amount is not None:
            validation_prompt_parts.append(f"Is {document_data.total_amount} a reasonable total amount for a receipt (i.e., positive number)?")

    if validation_prompt_parts:
        validation_prompt = "Please answer the following questions with a JSON object. For each question, provide a 'valid' boolean and a 'reason' string. For amounts, 'reasonable' means positive and non-zero. Example: {\"question\": \"Is X a valid date?\", \"valid\": true, \"reason\": \"Format matches\"}" + "\n\n" + "\n".join([f"- {q}" for q in validation_prompt_parts])
        
        try:
            openai_validation_response_str = call_openai_chat_model(client, model_deployment_name, validation_prompt)
            openai_validation_results = json.loads(openai_validation_response_str)
            
            if isinstance(openai_validation_results, list):
                for res in openai_validation_results:
                    question = res.get("question", "Unknown question")
                    is_valid = res.get("valid", False)
                    reason = res.get("reason", "")
                    
                    # Map back to original fields for ValidationResult
                    field_name_mapping = {
                        f"Is '{document_data.invoice_date}' a valid date in YYYY-MM-DD format?": "invoice_date",
                        f"Is '{document_data.transaction_date}' a valid date in YYYY-MM-DD format?": "transaction_date",
                        f"Is {document_data.total_amount} a reasonable total amount for an invoice (i.e., positive number)?": "total_amount",
                        f"Is {document_data.total_amount} a reasonable total amount for a receipt (i.e., positive number)?": "total_amount",
                    }
                    
                    original_field_name = field_name_mapping.get(question, "openai_validation")
                    validation_results.append(ValidationResult(
                        field_name=original_field_name,
                        is_valid=is_valid,
                        confidence=1.0 if is_valid else 0.5, # Lower confidence if OpenAI says it's not valid
                        message=f"OpenAI check: {reason}"
                    ))
            else:
                # Handle cases where OpenAI returns a single object or unexpected format
                print(f"Unexpected OpenAI validation response format: {openai_validation_response_str}")

        except json.JSONDecodeError as e:
            print(f"Error decoding OpenAI validation response: {e}")
        except Exception as e:
            print(f"Error during OpenAI validation call: {e}")

    return validation_results
