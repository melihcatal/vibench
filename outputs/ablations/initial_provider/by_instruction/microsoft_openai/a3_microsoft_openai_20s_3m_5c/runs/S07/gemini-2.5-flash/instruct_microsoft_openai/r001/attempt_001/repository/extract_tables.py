from document_client import get_document_intelligence_client
from document_models import ExtractedTable

def extract_tables_from_document(document_data: bytes, content_type: str) -> list[ExtractedTable]:
    client = get_document_intelligence_client()
    
    poller = client.begin_analyze_document(model_id="prebuilt-layout", document=document_data, content_type=content_type)
    result = poller.result()

    extracted_tables = []
    if result.tables:
        for table in result.tables:
            rows = []
            for row_idx in range(table.row_count):
                current_row = []
                for col_idx in range(table.column_count):
                    cell_content = ""
                    for cell in table.cells:
                        if cell.row_index == row_idx and cell.column_index == col_idx:
                            cell_content = cell.content
                            break
                    current_row.append({"content": cell_content})
                rows.append(current_row)
            
            bounding_box = []
            if table.bounding_regions:
                for region in table.bounding_regions:
                    # Assuming a simple case where we take the first bounding region, or combine them if necessary
                    # For simplicity, we'll just take the polygon points as a flat list
                    bounding_box.extend([p.x, p.y for p in region.polygon])

            extracted_tables.append(ExtractedTable(rows=rows, bounding_box=bounding_box, confidence=table.confidence))
    
    return extracted_tables
