from document_client import get_textract_client
from document_models import Table
from typing import List
import io

def extract_tables(image_path: str) -> List[Table]:
    client = get_textract_client()
    with io.open(image_path, 'rb') as image_file:
        img_bytes = image_file.read()
    response = client.analyze_document(
        Document={'Bytes': img_bytes},
        FeatureTypes=['TABLES']
    )
    tables = []
    cell_blocks = [b for b in response['Blocks'] if b['BlockType'] == 'CELL']
    if cell_blocks:
        row_indices = [int(b['RowIndex']) for b in cell_blocks]
        col_indices = [int(b['ColumnIndex']) for b in cell_blocks]
        max_row = max(row_indices) if row_indices else 0
        max_col = max(col_indices) if col_indices else 0
        rows = [['' for _ in range(max_col + 1)] for _ in range(max_row + 1)]
        for cell in cell_blocks:
            r = int(cell['RowIndex'])
            c = int(cell['ColumnIndex'])
            rows[r][c] = cell['Text']
        # bbox from table block or first cell
        table_bbox = {}
        if response['Blocks']:
            table_blocks = [b for b in response['Blocks'] if b['BlockType'] == 'TABLE']
            if table_blocks:
                geom = table_blocks[0]['Geometry']['BoundingBox']
                table_bbox = {
                    'top': geom['Top'],
                    'left': geom['Left'],
                    'width': geom['Width'],
                    'height': geom['Height']
                }
        tables.append(Table(rows=rows, bbox=table_bbox))
    return tables