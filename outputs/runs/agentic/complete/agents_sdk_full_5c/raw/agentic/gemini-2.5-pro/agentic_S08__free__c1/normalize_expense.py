import json
from document_client import get_anthropic_client
from document_models import NormalizedExpense, ExtractedInvoice, ExtractedReceipt


def normalize_expense(
    extracted_data: ExtractedInvoice | ExtractedReceipt,
) -> NormalizedExpense:
    """
    Normalizes extracted invoice or receipt data into a standard expense schema
    using Anthropic's Claude model.
    """
    client = get_anthropic_client()

    source_json = extracted_data.model_dump_json(indent=2)
    target_schema = NormalizedExpense.model_json_schema()

    prompt = f"""
        You are a data normalization expert. Your task is to convert a JSON object
        extracted from a document (invoice or receipt) into a standardized
        'NormalizedExpense' schema.

        Analyze the source JSON and map its fields to the target schema as accurately as possible.
        - 'vendor' should be the merchant or supplier name.
        - 'transaction_date' should be the main date on the document.
        - 'total' should be the final amount.
        - Populate 'line_items' from the source items.

        Respond with only the populated JSON object, without any surrounding text or markdown.

        Source JSON:
        {source_json}

        Target JSON Schema:
        {json.dumps(target_schema, indent=2)}

        Populated JSON object:
    """

    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=2048,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
    )

    response_text = message.content[0].text
    normalized_data = json.loads(response_text)

    return NormalizedExpense(**normalized_data)
