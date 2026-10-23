from google.cloud import vision

from document_client import vision_client
from document_models import DocumentRequest, TableResponse


def extract_tables(request: DocumentRequest) -> TableResponse:
    client = vision_client()
    with open(request.image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    result = client.document_text_detection(image=image)
    tables = []
    for page in (
        result.full_text_annotation.pages if result.full_text_annotation else []
    ):
        for block in page.blocks:
            if block.block_type == vision.Block.BlockType.TABLE:
                tables.append({"cells": [], "rows": []})
    return TableResponse(tables=tables)
