from typing import List
from document_client import get_document_client
from document_models import Paragraph


def extract_layout_from_url(document_url: str) -> List[Paragraph]:
    """
    Extracts layout elements (paragraphs) from a document at a given URL.
    Uses Azure AI Document Intelligence's "prebuilt-layout" model.
    """
    document_analysis_client = get_document_client()

    poller = document_analysis_client.begin_analyze_document_from_url(
        "prebuilt-layout", document_url
    )
    result = poller.result()

    extracted_paragraphs = []
    if result.paragraphs:
        for paragraph in result.paragraphs:
            extracted_paragraphs.append(
                Paragraph(
                    content=paragraph.content,
                    role=paragraph.role,
                    bounding_regions=[
                        (region.page_number, region.polygon)
                        for region in paragraph.bounding_regions
                    ],
                )
            )

    return extracted_paragraphs
