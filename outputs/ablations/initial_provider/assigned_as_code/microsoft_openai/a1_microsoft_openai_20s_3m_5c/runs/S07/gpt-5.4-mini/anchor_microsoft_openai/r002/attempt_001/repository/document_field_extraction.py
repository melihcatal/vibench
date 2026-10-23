import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def document_field_extraction(payload, config=None):
    config = config or {}
    endpoint = config.get('endpoint') or os.environ['AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT']
    api_key = config.get('api_key') or os.environ['AZURE_DOCUMENT_INTELLIGENCE_API_KEY']
    with DocumentIntelligenceClient(endpoint, AzureKeyCredential(api_key)) as client:
        result = client.begin_analyze_document('prebuilt-document', body=payload['document_bytes'], content_type=payload['mime_type']).result()
    return {'fields': getattr(result, 'fields', None)}
