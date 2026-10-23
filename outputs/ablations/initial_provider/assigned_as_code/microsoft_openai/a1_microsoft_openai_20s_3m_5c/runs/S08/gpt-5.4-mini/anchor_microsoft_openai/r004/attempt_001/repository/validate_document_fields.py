from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
import io


def validate_document_fields(payload, config=None):
    config = config or {}
    with DocumentIntelligenceClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.begin_analyze_document('prebuilt-document', body=io.BytesIO(payload['document_bytes']), content_type=payload['mime_type']).result()
    documents = []
    for document in result.documents or []:
        fields = document.fields or {}
        required = ['VendorName', 'InvoiceDate', 'InvoiceTotal']
        documents.append({'valid': all(name in fields and fields[name].confidence is not None for name in required), 'missing': [name for name in required if name not in fields], 'confidence': {name: fields[name].confidence if name in fields else None for name in required}})
    return {'validation': documents}
