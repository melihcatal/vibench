from document_client import get_document_intelligence_client
from document_models import ExtractedTable

def extract_tables_from_document(document_data: bytes) -> list[ExtractedTable]:
    client = get_document_intelligence_client()
    
    # Using prebuilt-read model for general document analysis which includes tables
    poller = client.begin_analyze_document(model_id="prebuilt-layout", document=document_data)
    result = poller.result()
    
    extracted_tables = []
    if result.tables:
        for table in result.tables:
            cells_data = []
            for cell in table.cells:
                cells_data.append({
                    "content": cell.content,
                    "row_index": cell.row_index,
                    "column_index": cell.column_index,
                    "row_span": cell.row_span,
                    "column_span": cell.column_span,
                    "bounding_regions": [{"page_number": br.page_number, "polygon": [(p.x, p.y) for p in br.polygon]} for br in cell.bounding_regions] if cell.bounding_regions else []
                })
            extracted_tables.append(ExtractedTable(
                cells=cells_data,
                row_count=table.row_count,
                column_count=table.column_count,
                page_number=table.bounding_regions[0].page_number if table.bounding_regions else None
            ))
                
    return extracted_tables
