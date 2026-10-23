from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from document_client import AzureDocumentIntelligenceClient
from document_models import LayoutBlock
from typing import List


def extract_layout_from_azure_di(
    file_content: bytes, mime_type: str
) -> List[LayoutBlock]:
    client = AzureDocumentIntelligenceClient().client

    poller = client.begin_analyze_document(
        model_id="prebuilt-layout", analyze_request=file_content, content_type=mime_type
    )
    result: AnalyzeResult = poller.result()

    layout_blocks: List[LayoutBlock] = []
    if result.pages:
        for page in result.pages:
            if page.lines:
                for line in page.lines:
                    layout_blocks.append(
                        LayoutBlock(
                            text=line.content,
                            bounding_boxes=[point.x for point in line.polygon]
                            + [point.y for point in line.polygon],
                            block_type="line",
                        )
                    )
            if page.words:
                for word in page.words:
                    layout_blocks.append(
                        LayoutBlock(
                            text=word.content,
                            bounding_boxes=[point.x for point in word.polygon]
                            + [point.y for point in word.polygon],
                            block_type="word",
                        )
                    )
    return layout_blocks
