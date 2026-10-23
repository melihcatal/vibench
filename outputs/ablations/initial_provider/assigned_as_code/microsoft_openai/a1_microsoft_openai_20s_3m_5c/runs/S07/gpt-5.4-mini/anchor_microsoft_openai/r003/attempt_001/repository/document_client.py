import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def load_config(config=None):
    config = config or {}
    return {
        'endpoint': config.get('endpoint') or os.environ['AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT'],
        'api_key': config.get('api_key') or os.environ['AZURE_DOCUMENT_INTELLIGENCE_API_KEY'],
    }


def get_client(config=None):
    cfg = load_config(config)
    return DocumentIntelligenceClient(cfg['endpoint'], AzureKeyCredential(cfg['api_key']))


def analyze_document(client, model_id, document_bytes, mime_type):
    return client.begin_analyze_document(
        model_id,
        body=document_bytes,
        content_type=mime_type,
    ).result()
