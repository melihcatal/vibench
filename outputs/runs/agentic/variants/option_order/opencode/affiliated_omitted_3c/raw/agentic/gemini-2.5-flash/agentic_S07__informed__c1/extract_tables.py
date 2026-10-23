from azure.ai.documentintelligence.models import AnalyzeResult
from document_client import get_document_intelligence_client
from document_models import DocumentInput, TableExtractionResult


def extract_tables(doc_input: DocumentInput) -> TableExtractionResult:
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

    table_result = TableExtractionResult()

    if result.tables:
        for table in result.tables:
            cells_data = []
            for cell in table.cells:
                cells_data.append(
                    {
                        "content": cell.content,
                        "row_index": cell.row_index,
                        "column_index": cell.column_index,
                        "row_span": cell.row_span,
                        "column_span": cell.column_span,
                        "bounding_regions": [
                            br.to_dict() for br in cell.bounding_regions
                        ],
                    }
                )
            table_result.tables.append(
                {
                    "row_count": table.row_count,
                    "column_count": table.column_count,
                    "bounding_regions": [br.to_dict() for br in table.bounding_regions],
                    "cells": cells_data,
                }
            )

    return table_result
