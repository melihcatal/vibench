import os
from azure.ai.documentintelligence.models import ContentFormat, AnalyzeResult
from document_client import get_azure_document_intelligence_client
from document_models import DocumentInput, LayoutExtractionResult, LayoutBlock, BoundingBox

def extract_layout_from_document(doc_input: DocumentInput) -> LayoutExtractionResult:
    client = get_azure_document_intelligence_client()

    poller = client.begin_analyze_document(
        model_id="prebuilt-layout",
        analyze_request=doc_input.document_bytes,
        content_type=doc_input.mime_type
    )
    result: AnalyzeResult = poller.result()

    extracted_blocks: list[LayoutBlock] = []
    
    if result.pages:
        for page in result.pages:
            if page.lines:
                for line in page.lines:
                    bbox = BoundingBox(
                        x1=min(p.x for p in line.polygon), 
                        y1=min(p.y for p in line.polygon),
                        x2=max(p.x for p in line.polygon),
                        y2=max(p.y for p in line.polygon)
                    ) if line.polygon else BoundingBox(0,0,0,0)
                    extracted_blocks.append(
                        LayoutBlock(
                            text_content=line.content,
                            block_type="line",
                            bounding_box=bbox,
                            confidence=line.confidence
                        )
                    )
            if page.paragraphs:
                for paragraph in page.paragraphs:
                    bbox = BoundingBox(
                        x1=min(p.x for p in paragraph.polygon), 
                        y1=min(p.y for p in paragraph.polygon),
                        x2=max(p.x for p in paragraph.polygon),
                        y2=max(p.y for p in paragraph.polygon)
                    ) if paragraph.polygon else BoundingBox(0,0,0,0)
                    extracted_blocks.append(
                        LayoutBlock(
                            text_content=paragraph.content,
                            block_type="paragraph",
                            bounding_box=bbox,
                            confidence=paragraph.confidence
                        )
                    )

    full_text = result.content if result.content else ""

    return LayoutExtractionResult(blocks=extracted_blocks, full_text=full_text)