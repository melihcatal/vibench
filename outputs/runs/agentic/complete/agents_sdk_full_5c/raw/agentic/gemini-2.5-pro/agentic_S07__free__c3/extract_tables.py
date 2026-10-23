import boto3
from document_client import get_aws_textract_client
from document_models import Table, TableCell, BoundingBox, Point
from typing import List

def extract_tables_from_document(document_path: str) -> List[Table]:
    """
    Extracts tables from a document image using Amazon Textract.
    
    Args:
        document_path: The local path to the document file.

    Returns:
        A list of Table objects found in the document.
    """
    textract_client = get_aws_textract_client()

    with open(document_path, "rb") as document:
        image_bytes = document.read()

    response = textract_client.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['TABLES']
    )

    blocks = response['Blocks']
    tables_by_id = {
        block['Id']: block for block in blocks if block['BlockType'] == 'TABLE'
    }
    cells_by_id = {
        block['Id']: block for block in blocks if block['BlockType'] == 'CELL'
    }
    words_by_id = {
        block['Id']: block for block in blocks if block['BlockType'] == 'WORD'
    }

    extracted_tables = []
    for table_id, table_block in tables_by_id.items():
        table_cells = []
        relationships = table_block.get('Relationships', [])
        for rel in relationships:
            if rel['Type'] == 'CHILD':
                for cell_id in rel['Ids']:
                    cell_block = cells_by_id.get(cell_id)
                    if not cell_block:
                        continue
                    
                    text = ""
                    if 'Relationships' in cell_block:
                        for child_rel in cell_block['Relationships']:
                             if child_rel['Type'] == 'CHILD':
                                text = ' '.join([words_by_id[word_id]['Text'] for word_id in child_rel['Ids']])

                    points = [Point(x=p['X'], y=p['Y']) for p in cell_block['Geometry']['Polygon']]
                    
                    table_cells.append(TableCell(
                        text=text,
                        row_index=cell_block['RowIndex'],
                        col_index=cell_block['ColumnIndex'],
                        row_span=cell_block.get('RowSpan', 1),
                        col_span=cell_block.get('ColumnSpan', 1)
                    ))
        
        geo = table_block['Geometry']
        table_bbox = BoundingBox(points=[Point(p['X'], p['Y']) for p in geo['Polygon']])
        
        extracted_tables.append(Table(
            cells=table_cells,
            bounding_box=table_bbox,
            row_count=max(c.row_index for c in table_cells) if table_cells else 0,
            column_count=max(c.col_index for c in table_cells) if table_cells else 0,
        ))

    return extracted_tables
