from document_client import get_textract_client
from document_models import DocumentInput, ExtractionResult

def extract_tables(document_input: DocumentInput) -> ExtractionResult:
    textract_client = get_textract_client()
    response = textract_client.analyze_document(
        Document={
            'S3Object': {
                'Bucket': document_input.s3_bucket,
                'Name': document_input.s3_key
            }
        },
        FeatureTypes=['TABLES']
    )

    tables = []
    for block in response['Blocks']:
        if block['BlockType'] == 'TABLE':
            table_data = {
                "id": block['Id'],
                "cells": []
            }
            # Assuming 'RELATIONSHIPS' contains child IDs for cells
            for relationship in block.get('Relationships', []):
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        # Find the cell block by ID
                        cell_block = next((b for b in response['Blocks'] if b['Id'] == child_id and b['BlockType'] == 'CELL'), None)
                        if cell_block:
                            table_data["cells"].append({
                                "id": cell_block['Id'],
                                "text": next((t['Text'] for t in response['Blocks'] if t['BlockType'] == 'WORD' and t['Id'] in cell_block.get('Relationships', [])[0].get('Ids', []) and t['Text'] is not None), ''),
                                "row_index": cell_block.get('RowIndex'),
                                "column_index": cell_block.get('ColumnIndex')
                            })
            tables.append(table_data)

    return ExtractionResult(tables=tables, raw_response=response)
