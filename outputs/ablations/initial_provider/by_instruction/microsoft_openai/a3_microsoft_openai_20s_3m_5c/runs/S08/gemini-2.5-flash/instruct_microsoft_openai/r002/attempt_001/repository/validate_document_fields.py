from document_client import DocumentClients
from document_models import NormalizedExpense
import json
from typing import Dict, Any

def validate_document_fields(expense_record: NormalizedExpense) -> NormalizedExpense:
    clients = DocumentClients()
    if not clients.openai_client:
        raise ValueError("OpenAI client not initialized.")

    required_fields = [
        "transaction_date",
        "vendor_merchant_name",
        "total_amount",
        "currency",
        "document_type",
    ]
    validation_results: Dict[str, Any] = {"missing_fields": [], "invalid_data": []}
    overall_status = "completed"

    # Basic structural validation first
    for field in required_fields:
        if not getattr(expense_record, field):
            validation_results["missing_fields"].append(field)
            overall_status = "failed"

    # Use OpenAI to perform more nuanced validation based on content and common sense
    prompt = f"""Review the following normalized expense record (JSON representation). Identify any potential issues such as inconsistent data, implausible values (e.g., negative amounts for total_amount or tax_amount, dates in the future for transaction_date), or formatting errors. Also, check if the document type is consistent with the presence of vendor/merchant names. For line items, check if total_price is consistent with quantity * unit_price. Provide a JSON object with a 'status' (either 'passed' or 'failed') and 'details' which is a list of strings describing any issues found. If no issues, 'details' should be an empty list.\n\nExpense Record: {json.dumps(expense_record.__dict__, default=str, indent=2)}\n"""

    chat_completion = clients.openai_client.chat.completions.create(
        model="gpt-4o-mini", # Using a capable model for validation
        messages=[
            {"role": "system", "content": "You are an AI assistant that validates structured expense records. You output ONLY a JSON object with a 'status' and 'details' field."},
            {"role": "user", "content": prompt}
        ],
        response_format={ "type": "json_object" }
    )

    llm_validation_output = json.loads(chat_completion.choices[0].message.content)

    if llm_validation_output.get("status") == "failed":
        overall_status = "failed"
        validation_results["invalid_data"].extend(llm_validation_output.get("details", []))

    expense_record.validation_status = overall_status
    expense_record.validation_details = validation_results

    return expense_record
