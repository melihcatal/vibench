from google.cloud import documentai_v1 as documentai

from document_models import OCRResponse


def document_field_extraction(
    response: OCRResponse, project_id: str, location: str, processor_id: str
) -> dict:
    client = documentai.DocumentProcessorServiceClient()
    name = client.processor_path(project_id, location, processor_id)
    raw_document = documentai.RawDocument(
        content=response.text.encode("utf-8"), mime_type="text/plain"
    )
    result = client.process_document(
        request={"name": name, "raw_document": raw_document}
    )
    entities = (
        result.document.entities if result.document and result.document.entities else []
    )
    return {entity.type_: entity.mention_text for entity in entities}
