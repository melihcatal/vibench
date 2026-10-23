"""Extract layout elements (blocks, lines, tables, paragraphs) from a document using Azure AI Document Intelligence."""

import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.core.credentials import AzureKeyCredential

from document_models import LayoutRequest, LayoutResponse, LayoutElement


class AzureLayoutExtractor:
    """Document layout extraction via Azure AI Document Intelligence SDK."""

    def __init__(self):
        self.endpoint = os.environ.get(
            "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
            "https://<your-resource>.cognitiveservices.azure.com/",
        )
        self.api_key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")
        self.credential = AzureKeyCredential(self.api_key)
        self.client = DocumentIntelligenceClient(
            endpoint=self.endpoint, credential=self.credential
        )

    def analyze_layout(self, document_bytes: bytes, content_type: str = "application/pdf") -> LayoutResponse:
        """Analyze document layout using Azure prebuilt-layout model."""
        poller = self.client.begin_analyze_document(
            "prebuilt-layout",
            document=document_bytes,
            content_type=content_type,
        )
        result: AnalyzeResult = poller.result()

        elements = []

        for page in result.pages or []:
            page_number = page.page_number or 0

            for line in page.lines or []:
                elements.append(
                    LayoutElement(
                        element_type="line",
                        text=line.content or "",
                        page_number=page_number,
                        bounding_polygon=line.polygon,
                        confidence=line.confidence if hasattr(line, "confidence") else None,
                    )
                )

            for word in page.words or []:
                elements.append(
                    LayoutElement(
                        element_type="word",
                        text=word.content or "",
                        page_number=page_number,
                        bounding_polygon=word.polygon,
                        confidence=word.confidence,
                    )
                )

        for table in result.tables or []:
            elements.append(
                LayoutElement(
                    element_type="table",
                    text="",
                    page_number=table.bounding_regions[0].page_number if table.bounding_regions else None,
                    bounding_polygon=None,
                    row_count=table.row_count,
                    column_count=table.column_count,
                    confidence=None,
                )
            )

        for paragraph in result.paragraphs or []:
            elements.append(
                LayoutElement(
                    element_type="paragraph",
                    text=paragraph.content or "",
                    page_number=paragraph.bounding_regions[0].page_number if paragraph.bounding_regions else None,
                    bounding_polygon=None,
                    role=paragraph.role,
                    confidence=None,
                )
            )

        return LayoutResponse(
            elements=elements,
            page_count=len(result.pages) if result.pages else 0,
            provider="azure-document-intelligence",
        )


def extract_layout_from_bytes(document_bytes: bytes, content_type: str = "application/pdf") -> LayoutResponse:
    """High-level helper: extract layout elements from document bytes via Azure Document Intelligence."""
    extractor = AzureLayoutExtractor()
    return extractor.analyze_layout(document_bytes, content_type=content_type)


def extract_layout_from_file(file_path: str) -> LayoutResponse:
    """High-level helper: extract layout elements from a local file via Azure Document Intelligence."""
    with open(file_path, "rb") as fh:
        document_bytes = fh.read()
    content_type = (
        "application/pdf"
        if file_path.lower().endswith(".pdf")
        else "image/png"
    )
    return extract_layout_from_bytes(document_bytes, content_type=content_type)
