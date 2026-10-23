from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def document_field_extraction(payload, config=None):
    config = config or {}
    with DocumentIntelligenceClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.begin_analyze_document('prebuilt-document', body=payload['document_bytes'], content_type=payload['mime_type']).result()
    fields = {}
    for name in (payload.get('fields') or []):
        value = result.documents[0].fields.get(name) if getattr(result, 'documents', None) else None
        fields[name] = getattr(value, 'content', None) if value else None
    return {'fields': fields}
