from typing import Dict, List, Optional
import os
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from document_client import get_google_vision_client
from document_models import TableResponse


def extract_tables(image_path: str) -> TableResponse:
    """Extract table cells and row structure from a document using Google Cloud Vision."""
    client = get_google_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision_v1.types.Image(content=content)
    features = [{"type_": vision_v1.Feature.Type.TABLE_DETECTION}]

    request = vision_v1.types.AnnotateImageRequest(image=image, features=features)
    response = client.annotate_image(request)

    if response.error.message:
        raise ValueError(f"Google Cloud Vision API error: {response.error.message}")

    tables = []
    for table in response.table_annotation:
        table_data = {
            "rows": [],
            "bounding_box": {
                "vertices": [
                    {"x": vertex.x, "y": vertex.y}
                    for vertex in table.bounding_box.vertices
                ]
            },
        }

        for row in table.rows:
            row_data = {
                "cells": [],
                "bounding_box": {
                    "vertices": [
                        {"x": vertex.x, "y": vertex.y}
                        for vertex in row.bounding_box.vertices
                    ]
                },
            }

            for cell in row.cells:
                cell_text = "".join(
                    [
                        symbol.text
                        for word in cell.detected_words
                        for symbol in word.symbols
                    ]
                )
                row_data["cells"].append(
                    {
                        "text": cell_text,
                        "row_span": cell.row_span,
                        "col_span": cell.col_span,
                        "bounding_box": {
                            "vertices": [
                                {"x": vertex.x, "y": vertex.y}
                                for vertex in cell.bounding_box.vertices
                            ]
                        },
                    }
                )

            table_data["rows"].append(row_data)

        tables.append(table_data)

    return TableResponse(
        tables=tables, provider="google_vision", model="table_detection"
    )
