from google.cloud import vision

from storage_client import load_config


def stored_document_ocr(payload, config=None):
    config = load_config(config)
    client = vision.ImageAnnotatorClient()
    gcs_source_uri = f"gs://{config['bucket']}/{payload['object_name']}"
    feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)
    gcs_source = vision.GcsSource(uri=gcs_source_uri)
    input_config = vision.InputConfig(gcs_source=gcs_source, mime_type=payload.get("mime_type", "application/pdf"))
    async_request = vision.AsyncAnnotateFileRequest(features=[feature], input_config=input_config)
    operation = client.async_batch_annotate_files(requests=[async_request])
    result = operation.result(timeout=payload.get("timeout_seconds"))
    texts = []
    for response in result.responses:
        for page in response.responses:
            texts.append(page.full_text_annotation.text)
    return {"text": "\n".join(t for t in texts if t)}
