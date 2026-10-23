# normalize_expense.py
import json
from document_client import get_anthropic_client
from document_models import NormalizedExpense, ExtractedInvoice, ExtractedReceipt

def normalize_expense_data(
    extracted_data: ExtractedInvoice | ExtractedReceipt,
    source_type: str
) -> NormalizedExpense:
    """
    Normalizes extracted document data into a standard expense schema using Anthropic Claude.
    """
    client = get_anthropic_client()
    
    target_schema = NormalizedExpense.model_json_schema()

    prompt = f"""
        You are a data normalization expert. Your task is to convert raw extracted data from a document
        into a structured JSON object that conforms to the provided schema.

        Source Data (`{source_type}`):
        ```json
        {extracted_data.model_dump_json(indent=2)}
        ```

        Target JSON Schema:
        ```json
        {json.dumps(target_schema, indent=2)}
        ```

        Instructions:
        1. Map the fields from the source data to the target schema fields.
        2. `vendor` should be the merchant or vendor name.
        3. `transaction_date` should be in YYYY-MM-DD format.
        4. Convert all monetary values to floats.
        5. The `source_document_type` should be '{source_type}'.
        6. If line items are present, normalize them into the `line_items` array.
        7. If a required field is missing from the source data, use a sensible default or omit it if it's optional.
        8. Respond ONLY with the valid JSON object. Do not include any explanatory text or markdown.
    """

    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=2048,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    response_json_str = message.content[0].text
    normalized_data = json.loads(response_json_str)

    return NormalizedExpense(**normalized_data)
