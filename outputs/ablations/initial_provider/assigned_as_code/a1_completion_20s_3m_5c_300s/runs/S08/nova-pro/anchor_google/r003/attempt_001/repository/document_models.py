from google.cloud import documentai


def document_models(payload):
    request = documentai.ProcessDocumentRequest(
        raw_document=documentai.RawDocument(content=payload["document_bytes"], mime_type=payload["mime_type"]))
    return request