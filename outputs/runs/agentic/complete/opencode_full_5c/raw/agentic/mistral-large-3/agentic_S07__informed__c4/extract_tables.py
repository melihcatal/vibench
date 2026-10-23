from google.cloud import documentai_v1 as documentai
import os
from typing import List, Dict, Any
from document_client import get_document_client
from document_models import Table, TableResponse


def extract_tables_from_image(
    image_path: str, mime_type: str = "image/png"
) -> TableResponse:
    """
    Extracts tables and their cell structures from a document using Google Document AI.

    Args:
        image_path: Path to the document image file.
        mime_type: MIME type of the image (e.g., "image/png", "image/jpeg").

    Returns:
        TableResponse containing extracted tables and metadata.
    """
    client = get_document_client("google")
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    location = os.getenv("GOOGLE_DOCUMENT_AI_LOCATION", "us")
    processor_id = os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_ID")

    if not all([project_id, processor_id]):
        raise ValueError(
            "Google Cloud project ID and processor ID must be set in environment variables."
        )

    processor_name = (
        f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    )

    with open(image_path, "rb") as image_file:
        image_content = image_file.read()

    request = {
        "name": processor_name,
        "raw_document": {"content": image_content, "mime_type": mime_type},
    }

    result = client.process_document(request=request)
    document = result.document

    tables = []
    for page in document.pages:
        for table in page.tables:
            rows = []
            for row in table.header_rows + table.body_rows:
                cells = []
                for cell in row.cells:
                    cells.append(
                        {
                            "text": cell.layout.text_anchor.content
                            if cell.layout.text_anchor
                            else "",
                            "row_span": cell.row_span,
                            "col_span": cell.col_span,
                            "confidence": cell.layout.confidence,
                        }
                    )
                rows.append({"cells": cells})

            tables.append(
                Table(
                    rows=rows,
                    bounding_box={
                        "vertices": [
                            {"x": vertex.x, "y": vertex.y}
                            for vertex in table.layout.bounding_poly.normalized_vertices
                        ]
                    },
                    confidence=table.layout.confidence,
                )
            )

    return TableResponse(
        tables=tables,
        pages=len(document.pages),
        provider="google_document_ai",
        model="pretrained-table-v2.0-2023-06-02",
    )
