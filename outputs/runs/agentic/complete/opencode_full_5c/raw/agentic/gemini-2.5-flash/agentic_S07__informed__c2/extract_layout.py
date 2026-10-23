import os
from typing import List

from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions

from document_client import get_documentai_client
from document_models import ExtractedLayoutElement


def extract_layout_from_document(
    project_id: str, location: str, processor_id: str, file_path: str, mime_type: str
) -> List[ExtractedLayoutElement]:
    """Extracts layout elements from a document using Google Document AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Document AI processor location (e.g., "us").
        processor_id: The ID of the layout parser processor to use.
        file_path: The path to the document file.
        mime_type: The MIME type of the document (e.g., "application/pdf").

    Returns:
        A list of ExtractedLayoutElement objects.
    """
    client = get_documentai_client()

    resource_name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image_file:
        content = image_file.read()

    raw_document = documentai.RawDocument(content=content, mime_type=mime_type)

    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)

    result = client.process_document(request=request)

    document = result.document
    extracted_elements: List[ExtractedLayoutElement] = []

    # Extract paragraphs (blocks)
    for page in document.pages:
        for paragraph in page.paragraphs:
            text_segment = paragraph.layout.text_anchor.text_segments[0]
            text_content = document.text[
                text_segment.start_index : text_segment.end_index
            ]
            bounding_box = []
            for vertex in paragraph.layout.bounding_poly.normalized_vertices:
                bounding_box.extend([vertex.x, vertex.y])
            extracted_elements.append(
                ExtractedLayoutElement(
                    type="paragraph",
                    text_content=text_content,
                    bounding_box=bounding_box,
                )
            )

        # Extract lines
        for paragraph in page.paragraphs:
            for line in paragraph.lines:
                text_segment = line.layout.text_anchor.text_segments[0]
                text_content = document.text[
                    text_segment.start_index : text_segment.end_index
                ]
                bounding_box = []
                for vertex in line.layout.bounding_poly.normalized_vertices:
                    bounding_box.extend([vertex.x, vertex.y])
                extracted_elements.append(
                    ExtractedLayoutElement(
                        type="line",
                        text_content=text_content,
                        bounding_box=bounding_box,
                    )
                )

    return extracted_elements
