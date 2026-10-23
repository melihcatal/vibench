import os
from google.cloud import documentai_v1beta3 as documentai
from document_client import get_documentai_client
from document_models import DocumentProcessingRequest, DocumentLayoutExtractionResponse

def extract_layout(request: DocumentProcessingRequest) -> DocumentLayoutExtractionResponse:
    """Extracts layout elements (blocks, lines) from a document using Google Document AI."""
    client = get_documentai_client()
    processor_name = client.processor_path(
        os.environ.get("GOOGLE_CLOUD_PROJECT"),
        os.environ.get("GOOGLE_CLOUD_LOCATION"),
        os.environ.get("GOOGLE_DOCUMENT_AI_PROCESSOR_ID_GENERAL") # Use a general processor
    )

    with open(request.document_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(
        content=image_content,
        mime_type=request.mime_type
    )

    request_docai = documentai.ProcessRequest(
        name=processor_name,
        raw_document=raw_document
    )

    result = client.process_document(request_docai)
    document = result.document

    paragraphs = []
    for page in document.pages:
        for paragraph in page.paragraphs:
            paragraphs.append(documentai.Document.to_json(paragraph))

    blocks = []
    for page in document.pages:
        for block in page.blocks:
            blocks.append(documentai.Document.to_json(block))
            
    lines = []
    for page in document.pages: # pylint: disable=unused-variable
        for paragraph in page.paragraphs:
            for line in paragraph.layout.text_anchor.text_segments:
                lines.append(document.text[int(line.start_index):int(line.end_index)])

    return DocumentLayoutExtractionResponse(
        text_content=document.text,
        paragraphs=paragraphs,
        blocks=blocks,
        lines=lines
    )
