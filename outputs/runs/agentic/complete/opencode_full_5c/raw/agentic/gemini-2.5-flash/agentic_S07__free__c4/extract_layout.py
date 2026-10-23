from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client
from document_models import DocumentInput, ExtractedLayout

PROJECT_ID = "YOUR_GOOGLE_CLOUD_PROJECT_ID"  # Replace with your project ID
LOCATION = "us"
PROCESSOR_ID = "YOUR_PROCESSOR_ID"  # e.g., "OCR_PROCESSOR_ID" or a custom processor ID


def extract_layout_from_document(document_input: DocumentInput) -> ExtractedLayout:
    client = get_documentai_client()

    processor_name = client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)

    # The Document AI SDK expects a raw_document object for processing
    raw_document = documentai.RawDocument(
        content=document_input.content, mime_type=document_input.mime_type
    )

    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)
    response = client.process_document(request=request)

    document = response.document

    # Extracting layout information (simplified for demonstration)
    blocks = []
    for page in document.pages:
        for block in page.blocks:
            blocks.append(
                {
                    "text_segments": [
                        {
                            "start_index": block.layout.text_anchor.text_segments[
                                0
                            ].start_index,
                            "end_index": block.layout.text_anchor.text_segments[
                                0
                            ].end_index,
                        }
                    ]
                }
            )
        for paragraph in page.paragraphs:
            blocks.append(
                {
                    "text_segments": [
                        {
                            "start_index": paragraph.layout.text_anchor.text_segments[
                                0
                            ].start_index,
                            "end_index": paragraph.layout.text_anchor.text_segments[
                                0
                            ].end_index,
                        }
                    ]
                }
            )

    lines = []
    for page in document.pages:
        for line in page.lines:
            lines.append(
                {
                    "text_segments": [
                        {
                            "start_index": line.layout.text_anchor.text_segments[
                                0
                            ].start_index,
                            "end_index": line.layout.text_anchor.text_segments[
                                0
                            ].end_index,
                        }
                    ]
                }
            )

    # Note: Full layout extraction involves more complex parsing of Document AI's rich response.
    # This example focuses on basic block and line extraction.

    return ExtractedLayout(blocks=blocks, lines=lines)
