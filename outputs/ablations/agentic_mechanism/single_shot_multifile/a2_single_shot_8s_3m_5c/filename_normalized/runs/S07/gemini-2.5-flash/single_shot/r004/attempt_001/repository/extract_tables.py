import os
import boto3
from document_client import get_aws_textract_client
from document_models import DocumentInput, TableExtractionResult, Table, TableCell, BoundingBox

def extract_tables_from_document(doc_input: DocumentInput) -> TableExtractionResult:
    client = get_aws_textract_client()

    response = client.analyze_document(
        Document={'Bytes': doc_input.document_bytes},
        FeatureTypes=['TABLES']
    )

    blocks = response['Blocks']
    tables_map = {}
    cells_map = {}
    words_map = {}

    for block in blocks:
        if block['BlockType'] == 'TABLE':
            tables_map[block['Id']] = block
        elif block['BlockType'] == 'CELL':
            cells_map[block['Id']] = block
        elif block['BlockType'] == 'WORD':
            words_map[block['Id']] = block

    extracted_tables: list[Table] = []

    for table_id, table_block in tables_map.items():
        table_cells: list[TableCell] = []
        
        table_bbox = None
        if 'Geometry' in table_block and 'BoundingBox' in table_block['Geometry']:
            bb = table_block['Geometry']['BoundingBox']
            table_bbox = BoundingBox(x1=bb['Left'], y1=bb['Top'], x2=bb['Left']+bb['Width'], y2=bb['Top']+bb['Height'])

        if 'Relationships' in table_block:
            for relationship in table_block['Relationships']:
                if relationship['Type'] == 'CHILD':
                    for cell_id in relationship['Ids']:
                        if cell_id in cells_map:
                            cell_block = cells_map[cell_id]
                            
                            cell_content = ""
                            if 'Relationships' in cell_block:
                                for cell_rel in cell_block['Relationships']:
                                    if cell_rel['Type'] == 'CHILD':
                                        content_ids = cell_rel['Ids']
                                        word_contents = [words_map[wid]['Text'] for wid in content_ids if wid in words_map]
                                        cell_content = " ".join(word_contents)

                            cell_bbox = None
                            if 'Geometry' in cell_block and 'BoundingBox' in cell_block['Geometry']:
                                bb = cell_block['Geometry']['BoundingBox']
                                cell_bbox = BoundingBox(x1=bb['Left'], y1=bb['Top'], x2=bb['Left']+bb['Width'], y2=bb['Top']+bb['Height'])

                            table_cells.append(
                                TableCell(
                                    content=cell_content,
                                    row_index=cell_block['RowIndex'],
                                    column_index=cell_block['ColumnIndex'],
                                    row_span=cell_block.get('RowSpan', 1),
                                    column_span=cell_block.get('ColumnSpan', 1),
                                    bounding_box=cell_bbox,
                                    is_header='COLUMN_HEADER' in cell_block.get('EntityTypes', []) or 'TABLE_TITLE' in cell_block.get('EntityTypes', [])
                                )
                            )
        
        extracted_tables.append(Table(cells=table_cells, bounding_box=table_bbox))

    return TableExtractionResult(tables=extracted_tables)