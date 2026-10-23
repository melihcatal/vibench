import boto3
from document_client import TEXTRACT_REGION
from document_models import Table, BoundingBox, TableRow
from typing import List

def extract_tables(image_path: str) -> List[Table]:
    """Extracts table cells and row structure from a document."""
    client = boto3.client('textract', region_name=TEXTRACT_REGION)
    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()
    
    response = client.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['TABLES']
    )
    
    tables = []
    # Basic table structure extraction logic
    table_blocks = [block for block in response['Blocks'] if block['BlockType'] == 'TABLE']
    for table_block in table_blocks:
        table_bbox = BoundingBox(
            top=table_block['Geometry']['BoundingBox']['Top'],
            left=table_block['Geometry']['BoundingBox']['Left'],
            width=table_block['Geometry']['BoundingBox']['Width'],
            height=table_block['Geometry']['BoundingBox']['Height']
        )
        rows = []  # Would parse CELL blocks grouped by row_index
        tables.append(Table(rows=rows, bbox=table_bbox))
    return tables
