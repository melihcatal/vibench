from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client
from document_models import DocumentInput, ExtractedTable

PROJECT_ID = "YOUR_GOOGLE_CLOUD_PROJECT_ID"  # Replace with your project ID
LOCATION = "us"
PROCESSOR_ID = (
    "YOUR_TABLE_PROCESSOR_ID"  # e.g., "pretrained-table-parsing-v1-2020-09-23"
)


def extract_tables_from_document(document_input: DocumentInput) -> ExtractedTable:
    client = get_documentai_client()

    processor_name = client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)

    raw_document = documentai.RawDocument(
        content=document_input.content, mime_type=document_input.mime_type
    )

    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)
    response = client.process_document(request=request)

    document = response.document

    all_rows = []
    for page in document.pages:
        for table in page.tables:
            table_rows = []
            header_row_values = []
            for header_cell in table.header_rows[0].cells:
                header_row_values.append(
                    document.text[
                        header_cell.layout.text_anchor.text_segments[
                            0
                        ].start_index : header_cell.layout.text_anchor.text_segments[
                            0
                        ].end_index
                    ]
                )
            if header_row_values:
                table_rows.append(header_row_values)

            for body_row in table.body_rows:
                row_values = []
                for cell in body_row.cells:
                    row_values.append(
                        document.text[
                            cell.layout.text_anchor.text_segments[
                                0
                            ].start_index : cell.layout.text_anchor.text_segments[
                                0
                            ].end_index
                        ]
                    )
                table_rows.append(row_values)
            all_rows.append(table_rows)

    return ExtractedTable(rows=all_rows)
