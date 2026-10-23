from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def get_config(config=None):
    config = config or {}
    return {
        'endpoint': config.get('endpoint') or config.get('azure_document_intelligence_endpoint'),
        'api_key': config.get('api_key') or config.get('azure_document_intelligence_key'),
        'translation_endpoint': config.get('translation_endpoint') or config.get('azure_translation_endpoint'),
        'translation_key': config.get('translation_key') or config.get('azure_translation_key'),
        'safety_endpoint': config.get('safety_endpoint') or config.get('azure_content_safety_endpoint'),
        'safety_key': config.get('safety_key') or config.get('azure_content_safety_key'),
        'embedding_endpoint': config.get('embedding_endpoint') or config.get('azure_openai_endpoint'),
        'embedding_key': config.get('embedding_key') or config.get('azure_openai_key'),
        'embedding_model': config.get('embedding_model') or config.get('azure_openai_embedding_model') or 'text-embedding-3-small',
    }


def get_document_client(config=None):
    cfg = get_config(config)
    return DocumentIntelligenceClient(cfg['endpoint'], AzureKeyCredential(cfg['api_key']))
