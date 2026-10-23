from typing import List, Optional
from google.cloud import documentai_v1
from google.api_core.client_options import ClientOptions
from document_client import (
    get_document_ai_client,
    get_document_ai_processor_path,
    normalize_document_ai_tables,
    GOOGLE_CLOUD_PROJECT_ID,
    DOCUMENT_AI_LOCATION,
)
from document_models import (
    TableRequest,
    TableResponse,
    TableCell,
    TableRow,
    normalize_table_response,
)


DOCUMENT_AI_ENDPOINT = "us-documentai.googleapis.com"
GOOGLE_DOCUMENT_AI_PROCESSOR_TYPE = "OCR_PROCESSOR"
GOOGLE_DOCUMENT_AI_MODEL = "builtin/latest"


def extract_tables_from_image(
    image_bytes: bytes,
    mime_type: str = "image/png",
    detect_headers: bool = True,
) -> TableResponse:
    client = get_document_ai_client()
    processor_path = get_document_ai_processor_path()
    import base64

    encoded_content = base64.b64encode(image_bytes).decode("utf-8")
    raw_document = documentai_v1.RawDocument(
        content=encoded_content, mime_type=mime_type
    )
    process_request = documentai_v1.ProcessRequest(
        name=processor_path, raw_document=raw_document
    )
    response = client.process_document(request=process_request)
    document = response.document
    tables_data = []
    for page in document.pages:
        for table in page.tables:
            table_data = []
            for row_idx, row in enumerate(table.table_rows):
                row_data = []
                for col_idx, cell in enumerate(row.cells):
                    cell_text = ""
                    if cell.layout and cell.layout.text_anchor:
                        for segment in cell.layout.text_anchor.text_segments:
                            cell_text += document.text[
                                segment.start_index : segment.end_index
                            ]
                    row_data.append(
                        {
                            "text": cell_text.strip(),
                            "row_span": cell.row_span,
                            "col_span": cell.col_span,
                            "confidence": cell.confidence,
                        }
                    )
                table_data.append(row_data)
            tables_data.append(table_data)
    return normalize_table_response(tables_data)


def extract_tables_from_gcs_uri(
    gcs_uri: str,
    mime_type: str = "application/pdf",
    detect_headers: bool = True,
) -> TableResponse:
    client = get_document_ai_client()
    processor_path = get_document_ai_processor_path()
    gcs_document = documentai_v1.GcsDocument(gcs_uri=gcs_uri, mime_type=mime_type)
    gcs_documents = documentai_v1.GcsDocuments(documents=[gcs_document])
    input_config = documentai_v1.BatchDocumentsInputConfig(gcs_documents=gcs_documents)
    output_config = documentai_v1.OutputConfig(
        gcs_destination=documentai_v1.GcsDestination(uri="gs://temp-output-bucket/")
    )
    request = documentai_v1.BatchProcessRequest(
        name=processor_path,
        input_documents=input_config,
        document_output_config=output_config,
    )
    operation = client.batch_process_documents(request=request)
    operation.result()
    return TableResponse(tables=[])


def extract_table_structure(
    image_bytes: bytes,
    mime_type: str = "image/png",
) -> List[dict]:
    client = get_document_ai_client()
    processor_path = get_document_ai_processor_path()
    import base64

    encoded_content = base64.b64encode(image_bytes).decode("utf-8")
    raw_document = documentai_v1.RawDocument(
        content=encoded_content, mime_type=mime_type
    )
    process_request = documentai_v1.ProcessRequest(
        name=processor_path, raw_document=raw_document
    )
    response = client.process_document(request=process_request)
    document = response.document
    table_structures = []
    for page in document.pages:
        for table in page.tables:
            header_row = []
            body_rows = []
            for row_idx, row in enumerate(table.table_rows):
                row_cells = []
                for cell in row.cells:
                    cell_text = ""
                    if cell.layout and cell.layout.text_anchor:
                        for segment in cell.layout.text_anchor.text_segments:
                            cell_text += document.text[
                                segment.start_index : segment.end_index
                            ]
                    row_cells.append(
                        {
                            "text": cell_text.strip(),
                            "row_span": cell.row_span,
                            "col_span": cell.col_span,
                            "confidence": cell.confidence,
                            "bounding_box": {
                                "vertices": [
                                    {"x": v.x, "y": v.y}
                                    for v in cell.layout.bounding_poly.normalized_vertices
                                ]
                                if cell.layout and cell.layout.bounding_poly
                                else []
                            },
                        }
                    )
                if row_idx == 0:
                    header_row = row_cells
                else:
                    body_rows.append(row_cells)
            table_structures.append(
                {
                    "headers": header_row,
                    "rows": body_rows,
                    "row_count": len(table.table_rows),
                    "col_count": max(len(r.cells) for r in table.table_rows)
                    if table.table_rows
                    else 0,
                }
            )
    return table_structures
