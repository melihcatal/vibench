import os
from typing import List
from mindee import Client, documents
from mindee.input import LocalInputSource
from .document_models import TableStructure, TableCell


def extract_tables_from_image(file_path: str) -> List[TableStructure]:
    """
    Extracts table structures from a document using Mindee OCR.
    Requires MINDEE_API_KEY environment variable.
    """
    api_key = os.getenv("MINDEE_API_KEY")
    if not api_key:
        raise ValueError("MINDEE_API_KEY environment variable not set")

    client = Client(api_key=api_key)
    input_source = LocalInputSource(file_path)
    response = client.parse(
        document_type=documents.TypeDocumentFile, input_source=input_source
    )

    tables = []
    for page in response.document.inference.pages:
        for table in page.tables:
            rows = []
            for row_idx, row in enumerate(table.rows):
                row_cells = []
                for col_idx, cell in enumerate(row.cells):
                    row_cells.append(
                        TableCell(
                            text=cell.value,
                            row_index=row_idx,
                            col_index=col_idx,
                            confidence=cell.confidence,
                            bounding_box={
                                "x1": cell.bounding_box[0][0],
                                "y1": cell.bounding_box[0][1],
                                "x2": cell.bounding_box[2][0],
                                "y2": cell.bounding_box[2][1],
                            },
                        )
                    )
                rows.append(row_cells)
            tables.append(TableStructure(rows=rows, confidence=table.confidence))

    return tables
