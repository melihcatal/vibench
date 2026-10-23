from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def validate_document_fields(payload, config=None):
    config = config or {}
    with DocumentIntelligenceClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.begin_analyze_document('prebuilt-layout',
            body=payload['document_bytes'], content_type=payload['mime_type']).result()
    documents = []
    for document in result.documents or []:
        fields = document.fields or {}
        documents.append({
            'required_fields_present': all(name in fields for name in ('VendorName', 'InvoiceDate', 'InvoiceTotal')),
            'confidence_scores': {name: fields[name].confidence if name in fields else 0.0 for name in ('VendorName', 'InvoiceDate', 'InvoiceTotal')},
        })
    return {'validation': documents}
