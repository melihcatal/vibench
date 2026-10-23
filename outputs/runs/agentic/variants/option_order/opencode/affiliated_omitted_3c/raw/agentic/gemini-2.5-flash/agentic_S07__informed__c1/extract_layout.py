from azure.ai.documentintelligence.models import AnalyzeResult
from document_client import get_document_intelligence_client
from document_models import DocumentInput, LayoutExtractionResult


def extract_layout(doc_input: DocumentInput) -> LayoutExtractionResult:
    client = get_document_intelligence_client()

    if doc_input.document_url:
        poller = client.begin_analyze_document(
            "prebuilt-layout", document_url=doc_input.document_url
        )
    elif doc_input.document_bytes and doc_input.content_type:
        poller = client.begin_analyze_document(
            "prebuilt-layout",
            analyze_request=doc_input.document_bytes,
            content_type=doc_input.content_type,
        )
    else:
        raise ValueError(
            "Either document_url or document_bytes with content_type must be provided."
        )

    result: AnalyzeResult = poller.result()

    layout_result = LayoutExtractionResult()

    if result.pages:
        for page in result.pages:
            if page.lines:
                for line in page.lines:
                    layout_result.lines.append(
                        {
                            "content": line.content,
                            "bounding_regions": [
                                br.to_dict() for br in line.bounding_regions
                            ],
                        }
                    )
            if page.words:
                for word in page.words:
                    layout_result.words.append(
                        {
                            "content": word.content,
                            "bounding_regions": [
                                br.to_dict() for br in word.bounding_regions
                            ],
                        }
                    )

    if result.tables:
        for table in result.tables:
            cells_data = []
            for cell in table.cells:
                cells_data.append(
                    {
                        "content": cell.content,
                        "row_index": cell.row_index,
                        "column_index": cell.column_index,
                    }
                )
            layout_result.tables.append(
                {
                    "row_count": table.row_count,
                    "column_count": table.column_count,
                    "cells": cells_data,
                }
            )

    # Azure Document Intelligence `prebuilt-layout` does not directly expose 'blocks' as a distinct concept like 'paragraphs'
    # but we can infer them from paragraphs if available or use lines as blocks for simplicity here.
    if result.paragraphs:
        for paragraph in result.paragraphs:
            layout_result.blocks.append(
                {
                    "content": paragraph.content,
                    "bounding_regions": [
                        br.to_dict() for br in paragraph.bounding_regions
                    ],
                }
            )

    return layout_result
