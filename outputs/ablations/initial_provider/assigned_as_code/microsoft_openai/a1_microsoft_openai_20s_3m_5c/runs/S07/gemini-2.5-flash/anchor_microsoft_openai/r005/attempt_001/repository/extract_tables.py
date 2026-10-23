
import os
import boto3
from document_client import get_textract_client
from document_models import DocumentTable, DocumentExtractionResult

def extract_tables(payload, config=None):
    config = config or {}
    client = get_textract_client()

    response = client.analyze_document(
        Document={
            'Bytes': payload['document_bytes']
        },
        FeatureTypes=['TABLES']
    )

    tables = []
    text_content = ""

    blocks = response['Blocks']
    block_map = {block['Id']: block for block in blocks}

    for block in blocks:
        if block['BlockType'] == 'PAGE':
            for relationship in block.get('Relationships', []):
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        child_block = block_map[child_id]
                        if child_block['BlockType'] == 'LINE':
                            text_content += child_block['Text'] + "\n"

        if block['BlockType'] == 'TABLE':
            rows = []
            table_bounding_boxes = [
                block['Geometry']['BoundingBox']['Left'],
                block['Geometry']['BoundingBox']['Top'],
                block['Geometry']['BoundingBox']['Width'],
                block['Geometry']['BoundingBox']['Height']
            ]

            for relationship in block.get('Relationships', []):
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        cell_block = block_map[child_id]
                        if cell_block['BlockType'] == 'CELL':
                            row_index = cell_block['RowIndex']
                            col_index = cell_block['ColumnIndex']
                            cell_text = ""
                            for cell_relationship in cell_block.get('Relationships', []):
                                if cell_relationship['Type'] == 'CHILD':
                                    for word_id in cell_relationship['Ids']:
                                        word_block = block_map[word_id]
                                        if word_block['BlockType'] == 'WORD':
                                            cell_text += word_block['Text'] + " "
                            
                            # Ensure rows list is large enough
                            while len(rows) < row_index:
                                rows.append([])
                            # Ensure current row is large enough
                            while len(rows[row_index - 1]) < col_index:
                                rows[row_index - 1].append("")

                            rows[row_index - 1][col_index - 1] = cell_text.strip()
            
            if rows:
                tables.append(DocumentTable(rows=rows, bounding_boxes=table_bounding_boxes))

    return DocumentExtractionResult(
        text_content=text_content,
        tables=tables
    )
