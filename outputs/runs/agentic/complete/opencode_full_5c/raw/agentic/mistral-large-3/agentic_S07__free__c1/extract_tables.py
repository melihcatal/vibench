from typing import List, Optional
import os
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from document_client import get_vision_client
from document_models import TableResponse, Table


def extract_tables(image_path: str) -> TableResponse:
    """Extract tables and their structure from a document using Google Cloud Vision."""
    client = get_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    features = [{"type_": vision_v1.Feature.Type.TABLE_DETECTION}]

    request = types.AnnotateImageRequest(image=image, features=features)
    response = client.annotate_image(request)

    tables = []
    for table in response.table_annotation.tables:
        tables.append(Table.from_vision_table(table))

    return TableResponse(tables=tables)
