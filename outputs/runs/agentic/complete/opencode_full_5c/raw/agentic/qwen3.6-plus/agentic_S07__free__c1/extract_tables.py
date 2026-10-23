from __future__ import annotations

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult

from document_client import get_document_client, AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT
from document_models import (
    DocumentRequest,
    TableResult,
    TableCell,
    BoundingBox,
    normalize_confidence,
    normalize_bounding_box,
)

AZURE_TABLE_MODEL_ID = "prebuilt-layout"


def extract_tables_from_document(
    request: DocumentRequest,
    client: DocumentIntelligenceClient | None = None,
) -> list[TableResult]:
    if client is None:
        client = get_document_client()

    doc_bytes = request.read_bytes()

    poller = client.begin_analyze_document(
        model_id=AZURE_TABLE_MODEL_ID,
        body={
            "base64Source": __import__("base64").b64encode(doc_bytes).decode("utf-8")
        },
        output_content_format="text",
    )
    result: AnalyzeResult = poller.result()

    table_results: list[TableResult] = []

    for page_idx, page in enumerate(result.pages or []):
        azure_tables = page.tables or []
        for azure_table in azure_tables:
            cells: list[TableCell] = []
            azure_cells = azure_table.cells or []

            for azure_cell in azure_cells:
                cell_text = azure_cell.content or ""
                confidence = normalize_confidence(azure_cell.confidence)
                bbox = normalize_bounding_box(azure_cell.polygon)

                is_header = False
                if hasattr(azure_cell, "kind") and azure_cell.kind:
                    is_header = (
                        "columnHeader" in azure_cell.kind
                        or "rowHeader" in azure_cell.kind
                    )

                cells.append(
                    TableCell(
                        row_index=azure_cell.row_index,
                        column_index=azure_cell.column_index,
                        text=cell_text,
                        confidence=confidence,
                        is_header=is_header,
                        row_span=azure_cell.row_span
                        if hasattr(azure_cell, "row_span") and azure_cell.row_span
                        else 1,
                        column_span=azure_cell.column_span
                        if hasattr(azure_cell, "column_span") and azure_cell.column_span
                        else 1,
                        bounding_box=bbox,
                    )
                )

            table_results.append(
                TableResult(
                    cells=cells,
                    row_count=azure_table.row_count,
                    column_count=azure_table.column_count,
                    page_number=page_idx + 1,
                    bounding_box=normalize_bounding_box(azure_table.polygon),
                )
            )

    return table_results


def extract_tables_from_file(
    file_path: str,
    content_type: str = "application/pdf",
) -> list[TableResult]:
    request = DocumentRequest.from_file(file_path, content_type)
    return extract_tables_from_document(request)


def extract_tables_from_url(
    url: str,
    client: DocumentIntelligenceClient | None = None,
) -> list[TableResult]:
    if client is None:
        client = get_document_client()

    poller = client.begin_analyze_document(
        model_id=AZURE_TABLE_MODEL_ID,
        body={"urlSource": url},
        output_content_format="text",
    )
    result: AnalyzeResult = poller.result()

    table_results: list[TableResult] = []

    for page_idx, page in enumerate(result.pages or []):
        for azure_table in page.tables or []:
            cells: list[TableCell] = []
            for azure_cell in azure_table.cells or []:
                is_header = False
                if hasattr(azure_cell, "kind") and azure_cell.kind:
                    is_header = (
                        "columnHeader" in azure_cell.kind
                        or "rowHeader" in azure_cell.kind
                    )

                cells.append(
                    TableCell(
                        row_index=azure_cell.row_index,
                        column_index=azure_cell.column_index,
                        text=azure_cell.content or "",
                        confidence=normalize_confidence(azure_cell.confidence),
                        is_header=is_header,
                        row_span=azure_cell.row_span
                        if hasattr(azure_cell, "row_span") and azure_cell.row_span
                        else 1,
                        column_span=azure_cell.column_span
                        if hasattr(azure_cell, "column_span") and azure_cell.column_span
                        else 1,
                        bounding_box=normalize_bounding_box(azure_cell.polygon),
                    )
                )

            table_results.append(
                TableResult(
                    cells=cells,
                    row_count=azure_table.row_count,
                    column_count=azure_table.column_count,
                    page_number=page_idx + 1,
                    bounding_box=normalize_bounding_box(azure_table.polygon),
                )
            )

    return table_results
