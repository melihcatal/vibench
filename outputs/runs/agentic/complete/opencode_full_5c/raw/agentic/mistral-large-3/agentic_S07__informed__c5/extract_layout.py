import os
from typing import List
from mindee import Client, documents
from mindee.input import LocalInputSource
from .document_models import LayoutBlock


def extract_layout_from_image(file_path: str) -> List[LayoutBlock]:
    """
    Extracts layout elements (blocks, lines, tables) from a document using Mindee OCR.
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

    blocks = []
    for page in response.document.inference.pages:
        for line in page.lines:
            blocks.append(
                LayoutBlock(
                    block_type="line",
                    bounding_box={
                        "x1": line.bounding_box[0][0],
                        "y1": line.bounding_box[0][1],
                        "x2": line.bounding_box[2][0],
                        "y2": line.bounding_box[2][1],
                    },
                    confidence=line.confidence,
                    text=line.value,
                )
            )
        for table in page.tables:
            blocks.append(
                LayoutBlock(
                    block_type="table",
                    bounding_box={
                        "x1": table.bounding_box[0][0],
                        "y1": table.bounding_box[0][1],
                        "x2": table.bounding_box[2][0],
                        "y2": table.bounding_box[2][1],
                    },
                    confidence=table.confidence,
                    rows=table.rows,
                )
            )

    return blocks
