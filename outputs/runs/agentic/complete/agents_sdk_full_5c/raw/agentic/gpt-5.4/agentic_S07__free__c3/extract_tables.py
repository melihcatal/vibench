from __future__ import annotations

from typing import Dict, List

from document_client import build_processor_name, get_documentai_client, get_processor_id, guess_mime_type
from document_models import DocumentRequest, TableCell, load_bytes, normalize_text
from google.cloud import documentai_v1 as documentai


def _layout_text(document: documentai.Document, layout: documentai.Document.Page.Layout) -> str:
    parts = []
    for segment in layout.text_anchor.text_segments:
        parts.append(document.text[int(segment.start_index):int(segment.end_index)])
    return normalize_text("".join(parts))


def extract_tables(request: DocumentRequest) -> List[Dict[str, List[TableCell]]]:
    client = get_documentai_client()
    processor_name = build_processor_name(get_processor_id("DOCUMENTAI_FORM_PARSER_PROCESSOR_ID"))
    raw_document = documentai.RawDocument(
        content=load_bytes(request.file_path),
        mime_type=guess_mime_type(request.file_path, request.mime_type),
    )
    result = client.process_document(
        request=documentai.ProcessRequest(name=processor_name, raw_document=raw_document)
    )
    document = result.document
    tables: List[Dict[str, List[TableCell]]] = []
    for page in document.pages:
        for table in page.tables:
            header_rows: List[TableCell] = []
            body_rows: List[TableCell] = []
            for r_idx, row in enumerate(table.header_rows):
                for c_idx, cell in enumerate(row.cells):
                    header_rows.append(
                        TableCell(
                            row_index=r_idx,
                            column_index=c_idx,
                            text=_layout_text(document, cell.layout),
                            row_span=cell.row_span,
                            column_span=cell.col_span,
                            confidence=cell.layout.confidence,
                        )
                    )
            for r_idx, row in enumerate(table.body_rows):
                for c_idx, cell in enumerate(row.cells):
                    body_rows.append(
                        TableCell(
                            row_index=r_idx,
                            column_index=c_idx,
                            text=_layout_text(document, cell.layout),
                            row_span=cell.row_span,
                            column_span=cell.col_span,
                            confidence=cell.layout.confidence,
                        )
                    )
            tables.append({"header_cells": header_rows, "body_cells": body_rows})
    return tables
