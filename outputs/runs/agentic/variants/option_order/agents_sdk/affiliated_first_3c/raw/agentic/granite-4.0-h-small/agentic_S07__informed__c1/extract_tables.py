import boto3

# Amazon Textract SDK integration for table extraction
client = boto3.client('textract')

def extract_tables_from_image(image_bytes):
    '''Extract table cells and row structure from a document using Amazon Textract.'''
    response = client.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['TABLES']
    )
    tables = []
    for block in response['Blocks']:
        if block['BlockType'] == 'TABLE':
            rows = []
            row_cells = []
            for relationship in block.get('Relationships', []):
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        child = next((b for b in response['Blocks'] if b['Id'] == child_id), None)
                        if child:
                            if child['BlockType'] == 'CELL':
                                cell_text = child.get('Text', '')
                                if child['ColumnIndex'] == 0:
                                    # start of new row
                                    if row_cells:
                                        rows.append(row_cells)
                                        row_cells = []
                                row_cells.append(cell_text)
            if row_cells:
                rows.append(row_cells)
            tables.append(rows)
    return tables
