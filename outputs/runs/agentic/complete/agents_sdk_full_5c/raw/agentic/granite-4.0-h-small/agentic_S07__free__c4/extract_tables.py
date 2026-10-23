# [SAME-SCENARIO] extract_tables.py

import os
from typing import List, Dict
from google.cloud import vision_v1
from .document_client import VisionClient
from .document_models import TableExtractionResponse

def extract_tables(image_bytes: bytes) -> TableExtractionResponse:
    """Extract tables from a document image using Google Cloud Vision Layout API.

    Args:
        image_bytes: raw image data.
    
    Returns:
        A TableExtractionResponse containing detected tables with cell structure.
    """
    client = VisionClient()
    image = vision_v1.types.Image(content=image_bytes)
    response = client.service.document_text_detection(image=image)
    tables = []
    for page in response.full_text_annotation.pages:
        for table in page.tables:
            cells = []
            for row in table.rows:
                for cell in row.cells:
                    cells.append({"content": cell.content, "row_index": cell.row_index, "col_index": cell.col_index})
            tables.append({"layout": cells, "row_count": table.rows_count, "col_count": table.columns_count})
    return TableExtractionResponse(tables=tables)
