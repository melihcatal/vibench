import boto3
import json
from typing import List, Dict
from document_models import Table
from document_client import load_document_image

def extract_tables(image_path: str) -> List[Table]:
    """
    Extract table structures using Amazon Textract.
    """
    client = boto3.client('textract', region_name=os.getenv('AWS_REGION', 'us-east-1'))

    response = client.analyze_document(
        Document={'Bytes': load_document_image(image_path)},
        FeatureTypes=['TABLES']
    )

    blocks = {block['Id']: block for block in response['Blocks']}
    tables: List[Table] = []

    for block in response['Blocks']:
        if block['BlockType'] == 'TABLE':
            table_cells: List[Dict] = []
            for relationship in block.get('Relationships', []):
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        cell = blocks.get(child_id)
                        if cell and cell['BlockType'] == 'CELL':
                            table_cells.append({
                                'row': cell.get('RowIndex', 0),
                                'column': cell.get('ColumnIndex', 0),
                                'text': cell.get('Text', ''),
                                'confidence': cell.get('Confidence')
                            })
            tables.append({'cells': table_cells})

    return tables
