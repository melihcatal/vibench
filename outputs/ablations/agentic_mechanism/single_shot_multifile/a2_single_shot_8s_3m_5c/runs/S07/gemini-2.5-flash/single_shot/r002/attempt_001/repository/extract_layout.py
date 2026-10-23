import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

from document_client import get_azure_document_intelligence_client
from document_models import ExtractedLayout, LayoutBlock, BoundingRegion

def extract_document_layout(document_content: bytes) -> ExtractedLayout:
    client = get_azure_document_intelligence_client()

    poller = client.begin_analyze_document(
        "prebuilt-layout", document_content
    )
    result = poller.result()

    blocks = []
    for page in result.pages:
        for line in page.lines:
            blocks.append(LayoutBlock(
                content=line.content,
                kind="line",
                bounding_regions=[BoundingRegion(
                    page_number=page.page_number,
                    polygon=list(line.polygon)
                )]
            ))
        for paragraph in page.paragraphs:
            blocks.append(LayoutBlock(
                content=paragraph.content,
                kind="paragraph",
                bounding_regions=[BoundingRegion(
                    page_number=page.page_number,
                    polygon=list(paragraph.polygon)
                )]
            ))

    return ExtractedLayout(blocks=blocks)
