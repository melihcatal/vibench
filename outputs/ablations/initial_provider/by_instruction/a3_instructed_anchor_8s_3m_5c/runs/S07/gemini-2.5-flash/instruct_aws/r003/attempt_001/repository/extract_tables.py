import base64
from typing import List
from document_client import get_textract_client
from document_models import DocumentTable, TableCell

def extract_tables_from_image(image_bytes: bytes) -> List[DocumentTable]:
    textract_client = get_textract_client()
    response = textract_client.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['TABLES']
    )

    tables = []
    blocks = response.get('Blocks', [])

    table_blocks = [block for block in blocks if block['BlockType'] == 'TABLE']

    for table_block in table_blocks:
        table_id = table_block['Id']
        cells: List[TableCell] = []
        rows = 0
        columns = 0

        for relationship in table_block.get('Relationships', []):
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    cell_block = next((b for b in blocks if b['Id'] == child_id and b['BlockType'] == 'CELL'), None)
                    if cell_block:
                        cell_text = "".join([b['Text'] for b in blocks if 'Id' in b and b['BlockType'] == 'WORD' and b['Id'] in cell_block.get('Relationships', [])[0].get('Ids', [])]) if cell_block.get('Relationships') else ''
                        cells.append(TableCell(
                            row_index=cell_block['RowIndex'],
                            column_index=cell_block['ColumnIndex'],
                            content=cell_text,
                            confidence=cell_block['Confidence']
                        ))
                        rows = max(rows, cell_block['RowIndex'])
                        columns = max(columns, cell_block['ColumnIndex'])

        tables.append(DocumentTable(
            id=table_id,
            cells=cells,
            rows=rows,
            columns=columns
        ))
    return tables
