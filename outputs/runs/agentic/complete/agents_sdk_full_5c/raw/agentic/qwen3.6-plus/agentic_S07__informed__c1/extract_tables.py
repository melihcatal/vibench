"""Extract table cells and row structure from a document using Google Cloud Document AI."""

import os
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions

from document_models import TableRequest, TableExtractionResponse, TableCell, TableRow


class GcpTableExtractor:
    """Table extraction via Google Cloud Document AI SDK."""

    def __init__(self):
        self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
        self.location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")
        self.processor_id = os.environ.get("GOOGLE_DOC_AI_PROCESSOR_ID", "")

        api_endpoint = f"{self.location}-documentai.googleapis.com"
        client_options = ClientOptions(api_endpoint=api_endpoint)

        self.client = documentai.DocumentProcessorServiceClient(client_options=client_options)
        self.name = self.client.processor_path(self.project_id, self.location, self.processor_id)

    def process_document(self, document_bytes: bytes, mime_type: str = "application/pdf") -> TableExtractionResponse:
        """Analyze a document with Google Document AI and extract table structures."""
        document = documentai.RawDocument(content=document_bytes, mime_type=mime_type)
        request = documentai.ProcessRequest(name=self.name, raw_document=document)

        result = self.client.process_document(request=request)
        document_obj = result.document

        tables = []
        page_tables = document_obj.pages[0].tables if document_obj.pages else []

        for table in page_tables:
            header_cells = []
            body_cells = []
            header_rows = []
            body_rows = []

            row_to_cells = {}

            for cell in table.body_cells:
                cell_text = self._get_text(cell.layout.text_anchor, document_obj.text)
                cell_obj = TableCell(
                    text=cell_text,
                    row_index=cell.row_index,
                    col_index=cell.column_index,
                    row_span=cell.row_span,
                    col_span=cell.column_span,
                    confidence=cell.confidence,
                )
                row_idx = cell.row_index
                if row_idx not in row_to_cells:
                    row_to_cells[row_idx] = []
                row_to_cells[row_idx].append(cell_obj)

            max_row = max(row_to_cells.keys()) if row_to_cells else 0

            header_row_count = table.header_rows if hasattr(table, "header_rows") else 0

            for row_idx in range(max_row + 1):
                cells_in_row = row_to_cells.get(row_idx, [])
                cells_in_row.sort(key=lambda c: c.col_index)
                row_obj = TableRow(cells=cells_in_row, row_index=row_idx)
                if row_idx < header_row_count:
                    header_rows.append(row_obj)
                else:
                    body_rows.append(row_obj)

            table_obj = {
                "header_rows": header_rows,
                "body_rows": body_rows,
                "total_rows": len(header_rows) + len(body_rows),
                "page_number": table.page_number,
            }
            tables.append(table_obj)

        return TableExtractionResponse(
            tables=tables,
            page_count=len(document_obj.pages) if document_obj.pages else 0,
            provider="google-document-ai",
        )

    @staticmethod
    def _get_text(text_anchor, document_text: str) -> str:
        if not text_anchor or not text_anchor.text_segments:
            return ""
        text = ""
        for segment in text_anchor.text_segments:
            start = int(segment.start_index)
            end = int(segment.end_index)
            text += document_text[start:end]
        return text.strip()


def extract_tables_from_bytes(document_bytes: bytes, mime_type: str = "application/pdf") -> TableExtractionResponse:
    """High-level helper: extract tables from document bytes via Google Document AI."""
    extractor = GcpTableExtractor()
    return extractor.process_document(document_bytes, mime_type=mime_type)


def extract_tables_from_file(file_path: str) -> TableExtractionResponse:
    """High-level helper: extract tables from a local file via Google Document AI."""
    with open(file_path, "rb") as fh:
        document_bytes = fh.read()
    mime_type = (
        "application/pdf"
        if file_path.lower().endswith(".pdf")
        else "image/png"
    )
    return extract_tables_from_bytes(document_bytes, mime_type=mime_type)
