from google.cloud import documentai_v1 as documentai

from document_client import build_documentai_name, load_config
from document_models import DocumentInput, KeyValuePair, normalize_text


def extract_key_values(document: DocumentInput):
    config = load_config()
    client = documentai.DocumentProcessorServiceClient()
    name = build_documentai_name(config.gcp_project_id, config.gcp_location, config.gcp_form_processor_id or config.gcp_processor_id)
    request = documentai.ProcessRequest(name=name, raw_document=documentai.RawDocument(content=document.content, mime_type=document.mime_type))
    response = client.process_document(request=request)
    pairs = []
    for page in getattr(response.document, "pages", []):
        for kv in getattr(page, "form_fields", []):
            key = normalize_text(getattr(kv.field_value, "text_anchor", None) or "")
            value = normalize_text(getattr(kv.field_value, "text_anchor", None) or "")
            pairs.append(KeyValuePair(key=key, value=value))
    return [{"key": p.key, "value": p.value} for p in pairs]
