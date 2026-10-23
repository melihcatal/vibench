from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client, get_project_id, get_location, DOCUMENT_AI_PROCESSOR_FORM_PARSER
from document_models import Table, TableCell

def extract_tables_from_document(document_bytes: bytes, mime_type: str) -> list[Table]:
    project_id = get_project_id()
    location = get_location()
    processor_id = DOCUMENT_AI_PROCESSOR_FORM_PARSER
    client = get_documentai_client()
    processor_name = client.processor_path(project_id, location, processor_id)
    raw_document = documentai.RawDocument(content=document_bytes, mime_type=mime_type)
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)
    response = client.process_document(request=request)
    document = response.document
    extracted_tables: list[Table] = []
    def get_text_from_span(text_segments, document_text):
        if not text_segments:
            return ""
        start_index = text_segments[0].start_index
        end_index = text_segments[0].end_index
        return document_text[start_index:end_index] if start_index is not None and end_index is not None else ""
    def convert_bounding_poly(bounding_poly) -> list[list[int]]:
        if not bounding_poly or not bounding_poly.vertices:
            return []
        return [[vertex.x, vertex.y] for vertex in bounding_poly.vertices]
    for page in document.pages:
        for documentai_table in page.tables:
            header_rows_data: list[list[TableCell]] = []
            body_rows_data: list[list[TableCell]] = []
            for row in documentai_table.header_rows:
                current_row_cells: list[TableCell] = []
                for cell in row.cells:
                    cell_text = get_text_from_span(cell.layout.text_anchor.text_segments, document.text)
                    current_row_cells.append(TableCell(
                        row_index=cell.row_index,
                        column_index=cell.column_index,
                        text_content=cell_text,
                        row_span=cell.row_span,
                        column_span=cell.column_span,
                        bounding_boxes=convert_bounding_poly(cell.layout.bounding_poly)
                    ))
                header_rows_data.append(current_row_cells)
            for row in documentai_table.body_rows:
                current_row_cells: list[TableCell] = []
                for cell in row.cells:
                    cell_text = get_text_from_span(cell.layout.text_anchor.text_segments, document.text)
                    current_row_cells.append(TableCell(
                        row_index=cell.row_index,
                        column_index=cell.column_index,
                        text_content=cell_text,
                        row_span=cell.row_span,
                        column_span=cell.column_span,
                        bounding_boxes=convert_bounding_poly(cell.layout.bounding_poly)
                    ))
                body_rows_data.append(current_row_cells)
            extracted_tables.append(Table(
                header_rows=header_rows_data,
                body_rows=body_rows_data,
                bounding_boxes=convert_bounding_poly(documentai_table.layout.bounding_poly),
                caption=None
            ))
    return extracted_tables