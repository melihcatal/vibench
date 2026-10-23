from typing import Dict, List, Optional
import os
from google.cloud import documentai_v1 as documentai
from document_client import get_document_processor_client
from document_models import TableResponse


def extract_tables(
    image_path: str, processor_id: Optional[str] = None
) -> TableResponse:
    """Extract tables from a document using Google Cloud Document AI."""
    client = get_document_processor_client()
    processor_name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT_ID')}/locations/us/processors/{processor_id or os.getenv('GOOGLE_DOCUMENT_AI_PROCESSOR_ID')}"

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    request = {
        "name": processor_name,
        "raw_document": {
            "content": content,
            "mime_type": "application/pdf"
            if image_path.endswith(".pdf")
            else "image/png",
        },
    }

    result = client.process_document(request=request)
    document = result.document

    tables = []
    for table in document.tables:
        rows = []
        for row in table.header_rows:
            rows.append(
                {
                    "cells": [
                        {
                            "text": cell.content,
                            "bounding_box": {
                                "vertices": [
                                    {"x": vertex.x, "y": vertex.y}
                                    for vertex in cell.layout.bounding_poly.vertices
                                ]
                            },
                        }
                        for cell in row.cells
                    ]
                }
            )
        for row in table.body_rows:
            rows.append(
                {
                    "cells": [
                        {
                            "text": cell.content,
                            "bounding_box": {
                                "vertices": [
                                    {"x": vertex.x, "y": vertex.y}
                                    for vertex in cell.layout.bounding_poly.vertices
                                ]
                            },
                        }
                        for cell in row.cells
                    ]
                }
            )

        tables.append(
            {
                "rows": rows,
                "bounding_box": {
                    "vertices": [
                        {"x": vertex.x, "y": vertex.y}
                        for vertex in table.layout.bounding_poly.vertices
                    ]
                },
            }
        )

    return TableResponse(tables=tables)
