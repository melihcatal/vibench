from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions
from typing import Dict, Any, List, Optional
from document_models import ExtractedReceipt

# Replace with your actual project ID, location, and processor ID
PROJECT_ID = 'your-gcp-project-id'
LOCATION = 'us'  # e.g., 'us' or 'eu'
PROCESSOR_ID = 'your-receipt-processor-id'  # e.g., 'receipt-parser-001'

# The full resource name of the processor
# e.g.: projects/project_id/locations/location/processors/processor_id
PROCESSOR_NAME = f'projects/{PROJECT_ID}/locations/{LOCATION}/processors/{PROCESSOR_ID}'

def extract_receipt_fields(image_bytes: bytes) -> ExtractedReceipt:
    client_options = ClientOptions(api_endpoint=f'{LOCATION}-documentai.googleapis.com')
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    # Read the file into memory
    raw_document = documentai.RawDocument(
        content=image_bytes,
        mime_type='application/pdf' # or 'image/jpeg', 'image/png'
    )

    # Configure the process request
    request = documentai.ProcessRequest(
        name=PROCESSOR_NAME,
        raw_document=raw_document,
    )

    result = client.process_document(request=request)
    document = result.document

    merchant_name: Optional[str] = None
    tax_amount: Optional[float] = None
    total_amount: Optional[float] = None
    items: List[Dict[str, Any]] = []

    for entity in document.entities:
        if entity.type == 'merchant_name':
            merchant_name = entity.mention_text
        elif entity.type == 'total_amount':
            try:
                total_amount = float(entity.mention_text)
            except ValueError:
                pass
        elif entity.type == 'tax_amount':
            try:
                tax_amount = float(entity.mention_text)
            except ValueError:
                pass
        elif entity.type == 'line_item':
            item_data = {}
            for prop in entity.properties:
                if prop.type == 'description':
                    item_data['description'] = prop.mention_text
                elif prop.type == 'amount':
                    try:
                        item_data['amount'] = float(prop.mention_text)
                    except ValueError:
                        pass
            if item_data:
                items.append(item_data)

    return ExtractedReceipt(
        merchant_name=merchant_name,
        tax_amount=tax_amount,
        total_amount=total_amount,
        items=items
    )
