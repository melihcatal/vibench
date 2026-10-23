import boto3
from document_client import get_textract_client
from document_models import ExtractedTable, ExtractedTableCell
from typing import List, Dict, Any

def extract_tables(image_bytes: bytes) -> List[ExtractedTable]:
    """
    Extracts table cells and row structure from a document using AWS Textract.
    """
    textract_client = get_textract_client()
    response = textract_client.analyze_document(
        Document={'Bytes': image_bytes},
        Features=['TABLES']
    )

    tables: List[ExtractedTable] = []
    blocks = response.get('Blocks', [])
    
    # Helper to find text for a block ID
    block_map = {block['Id']: block for block in blocks}

    for block in blocks:
        if block['BlockType'] == 'TABLE':
            table_cells: List[ExtractedTableCell] = []
            for relationship in block.get('Relationships', []):
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        cell_block = block_map.get(child_id)
                        if cell_block and cell_block['BlockType'] == 'CELL':
                            # Find text content for the cell
                            cell_text = ""
                            for cell_rel in cell_block.get('Relationships', []):
                                if cell_rel['Type'] == 'CHILD':
                                    for word_id in cell_rel['Ids']:
                                        word_block = block_map.get(word_id)
                                        if word_block and word_block['BlockType'] == 'WORD':
                                            cell_text += word_block.get('Text', '') + " "
                            cell_text = cell_text.strip()

                            table_cells.append(ExtractedTableCell(
                                text=cell_text,
                                row_index=cell_block['RowIndex'],
                                column_index=cell_block['ColumnIndex'],
                                row_span=cell_block.get('RowSpan', 1),
                                column_span=cell_block.get('ColumnSpan', 1),
                                confidence=cell_block.get('Confidence')
                            ))
            tables.append(ExtractedTable(
                cells=table_cells,
                geometry=block.get('Geometry'),
                confidence=block.get('Confidence')
            ))
    return tables
