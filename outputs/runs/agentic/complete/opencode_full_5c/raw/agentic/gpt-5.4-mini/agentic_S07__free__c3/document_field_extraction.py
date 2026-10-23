from google.cloud import documentai_v1 as documentai


def document_field_extraction(text):
    client = documentai.DocumentProcessorServiceClient()
    return {"text": text, "processor": client.transport._host}
