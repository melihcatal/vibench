
from document_client import get_document_intelligence_client
from document_models import DocumentFile, ExtractedTables, ExtractedTable

def extract_tables_from_document(doc: DocumentFile) -> ExtractedTables:
    """
    Extracts tables from a document image using Azure Document Intelligence.
    """
    client = get_document_intelligence_client()

    poller = None
    if doc.file_bytes:
        poller = client.begin_analyze_document(
            "prebuilt-layout",
            doc.file_bytes,
            content_type="application/octet-stream"
        )
    elif doc.file_url:
        poller = client.begin_analyze_document(
            "prebuilt-layout", {"urlSource": doc.file_url}
        )
    else:
        raise ValueError("DocumentFile must have file_bytes or file_url.")

    result = poller.result()
    
    extracted_tables = []
    if result.tables:
        for table in result.tables:
            extracted_tables.append(
                ExtractedTable(
                    row_count=table.row_count,
                    column_count=table.column_count,
                    cells=[
                        {
                            "row_index": cell.row_index,
                            "column_index": cell.column_index,
                            "content": cell.content,
                        }
                        for cell in table.cells
                    ],
                )
            )

    return ExtractedTables(tables=extracted_tables, raw_response=result)
