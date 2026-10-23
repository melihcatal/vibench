# normalize_expense.py
import json
from document_client import get_openai_client
from document_models import ExtractedInvoice, ExtractedReceipt, NormalizedExpense
from dataclasses import asdict

def normalize_to_expense(
    document: ExtractedInvoice | ExtractedReceipt,
    doc_hash: str,
    category_hint: str = "General"
) -> NormalizedExpense:
    """
    Normalizes extracted document data into a standard expense schema using OpenAI.
    """
    client = get_openai_client()
    doc_type = "invoice" if isinstance(document, ExtractedInvoice) else "receipt"

    prompt = f"""
    You are an expert accounting assistant. Your task is to normalize the following JSON data from a document into a standardized expense format.
    The output must be a single, valid JSON object that conforms to the NormalizedExpense schema.

    Document Type: {doc_type}
    Category Hint: {category_hint}
    Source Document Hash: {doc_hash}
    
    Input JSON:
    {json.dumps(asdict(document), indent=2)}

    Desired Output JSON Schema:
    {{
      "vendor": "string",
      "transaction_date": "YYYY-MM-DD",
      "total": "float",
      "currency": "string (e.g., USD, EUR)",
      "category": "string",
      "line_items": "[{{'description': 'string', 'amount': 'float'}}]",
      "source_document_type": "{doc_type}",
      "source_document_hash": "{doc_hash}"
    }}

    Please analyze the input JSON and generate the normalized expense JSON object.
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.1
    )

    content = response.choices[0].message.content
    if not content:
        raise ValueError("Failed to get a valid response from OpenAI.")

    normalized_data = json.loads(content)
    
    return NormalizedExpense(**normalized_data)
