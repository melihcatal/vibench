import io
import json
from document_client import get_aws_textract_client
from document_models import DocumentPayload, ReceiptExtractionResult, LineItem

def extract_receipt_fields(payload: DocumentPayload, config: dict = None) -> dict:
    config = config or {}
    client = get_aws_textract_client(config)

    response = client.analyze_document(
        Document={'Bytes': payload.document_bytes},
        FeatureTypes=['FORMS', 'TABLES']
    )

    # Basic parsing for receipt fields - this is a simplification
    # In a real scenario, more sophisticated parsing of Textract's block-based output would be needed
    # For this exercise, we will look for common fields in the detected forms.

    merchant_name = None
    total_amount = None
    tax_amount = None
    line_items = []

    # A simplified approach to extract fields. Textract's output is complex.
    # For a robust solution, one would iterate through blocks and relationships.
    # Here, we'll try to find common key-value pairs.
    if 'Blocks' in response:
        key_values = {}
        for block in response['Blocks']:
            if block['BlockType'] == 'KEY_VALUE_SET':
                if 'EntityType' in block and block['EntityType'] == 'KEY':
                    key_text = "".join([t['Text'] for t in block['Geometry']['TextDetections'] if 'TextDetections' in block['Geometry']]).strip()
                    value_block = next((b for b in response['Blocks'] if b['BlockType'] == 'KEY_VALUE_SET' and 'EntityTypes' in b and 'VALUE' in b['EntityTypes'] and block['Id'] in b['Relationships'][0]['Ids']), None)
                    if value_block:
                        value_text = "".join([t['Text'] for t in value_block['Geometry']['TextDetections'] if 'TextDetections' in value_block['Geometry']]).strip()
                        key_values[key_text.lower()] = value_text

        # Attempt to map common receipt fields
        merchant_name = key_values.get('merchant name') or key_values.get('vendor') or key_values.get('store')
        total_amount = key_values.get('total') or key_values.get('grand total')
        tax_amount = key_values.get('tax') or key_values.get('sales tax')

        # Line items are much harder to extract robustly without custom parsing logic
        # For simplicity, we'll leave line_items empty or add a placeholder.
        # A real solution would involve iterating through TABLE blocks or using custom models.

    return ReceiptExtractionResult(
        merchant=merchant_name,
        tax=tax_amount,
        total=total_amount,
        items=line_items,
        original_data=response
    ).dict()
