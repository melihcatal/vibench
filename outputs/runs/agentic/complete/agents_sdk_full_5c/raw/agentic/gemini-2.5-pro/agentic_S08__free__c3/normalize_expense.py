import os
import json
import cohere
from typing import Union

from document_models import ExtractedInvoice, ExtractedReceipt, NormalizedExpense


def normalize_with_cohere(
    extracted_data: Union[ExtractedInvoice, ExtractedReceipt],
    source_document_id: str,
) -> NormalizedExpense:
    """
    Normalizes extracted invoice or receipt data into a standard expense schema
    using the Cohere Command R model.
    """
    co = cohere.Client(os.environ.get("COHERE_API_KEY"))

    if isinstance(extracted_data, ExtractedInvoice):
        expense_type = "INVOICE"
        vendor = extracted_data.vendor_name
        date = extracted_data.invoice_date
        total = extracted_data.total_amount
        notes = f"Invoice ID: {extracted_data.invoice_id}"
    elif isinstance(extracted_data, ExtractedReceipt):
        expense_type = "RECEIPT"
        vendor = extracted_data.merchant_name
        date = extracted_data.transaction_date
        total = extracted_data.total
        notes = f"Receipt from {vendor}"
    else:
        raise TypeError("Unsupported data type for normalization.")

    prompt = f"""
    Given the following extracted expense data, please normalize it into the provided JSON schema.
    The output must be only the JSON object, with no other text.

    **Extracted Data:**
    ```json
    {json.dumps(extracted_data.model_dump(), indent=2)}
    ```

    **Target JSON Schema:**
    ```json
    {json.dumps(NormalizedExpense.model_json_schema(), indent=2)}
    ```

    **Instructions:**
    - `expense_id` should be a new unique ID. Use the source document ID with a prefix.
    - `vendor` should be the merchant or vendor name.
    - `transaction_date` should be the main date from the document.
    - `total` should be the final total amount.
    - `expense_type` should be '{expense_type}'.
    - `items` should be a list of line items or receipt items, mapped to the schema.
    - `source_document_id` should be '{source_document_id}'.
    - `currency_code` should be 'USD' unless specified otherwise.
    """

    response = co.chat(
        model="command-r",
        message=prompt,
        temperature=0.1,
    )

    normalized_json = json.loads(response.text)
    
    return NormalizedExpense(**normalized_json)
