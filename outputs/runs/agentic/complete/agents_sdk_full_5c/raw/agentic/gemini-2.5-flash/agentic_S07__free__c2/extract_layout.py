from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client
from document_models import DocumentProcessingRequest, LayoutExtractionResponse, LayoutBlock

def extract_layout(request: DocumentProcessingRequest) -> LayoutExtractionResponse:
    """Extracts layout elements (blocks, paragraphs, lines) from a document using Google Cloud Document AI.
    This typically uses a Form Parser or general-purpose processor that returns layout information.
    """
    client = get_documentai_client()

    # FORM_PARSER_PROCESSOR_V1 is a good general-purpose processor that provides layout information.
    processor_id = "FORM_PARSER_PROCESSOR_V1"  
    name = client.processor_path(request.project_id, request.location, processor_id)

    document = documentai.RawDocument(content=request.file_content, mime_type=request.mime_type)

    response = client.process_document(
        name=name,
        raw_document=document
    )

    extracted_blocks = []
    for page in response.document.pages:
        for paragraph in page.paragraphs:
            extracted_blocks.append(LayoutBlock(text_content=paragraph.layout.text_anchor.text_segments[0].text_content if paragraph.layout.text_anchor.text_segments else "", 
                                                block_type="paragraph"))
        for line in page.lines:
            extracted_blocks.append(LayoutBlock(text_content=line.layout.text_anchor.text_segments[0].text_content if line.layout.text_anchor.text_segments else "", 
                                                block_type="line"))

    # Note: More sophisticated parsing would be needed to extract full bounding boxes and richer layout info.
    # This example focuses on demonstrating the use of Document AI for layout segments.

    return LayoutExtractionResponse(layout_blocks=extracted_blocks)
