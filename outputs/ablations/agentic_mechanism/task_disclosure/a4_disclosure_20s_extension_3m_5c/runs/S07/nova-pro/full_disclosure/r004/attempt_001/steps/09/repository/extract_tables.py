import boto3

def extract_tables(document_path):
    textract_client = boto3.client('textract')
    with open(document_path, 'rb') as document:
        image_bytes = document.read()
    response = textract_client.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['TABLES']
    )
    tables = []
    for table in response.get('Blocks', []):
        if table['BlockType'] == 'TABLE':
            table_data = {
                'Cells': [],
                'Rows': []
            }
            for relationship in table.get('Relationships', []):
                if relationship['Type'] == 'CHILD':
                    cell_ids = [child_id for child_id in relationship['Ids']]
                    for cell in response['Blocks']:
                        if cell['Id'] in cell_ids and cell['BlockType'] == 'CELL':
                            table_data['Cells'].append({
                                'Text': cell.get('Text', ''),
                                'Column': cell.get('ColumnIndex', 0),
                                'Row': cell.get('RowIndex', 0)
                            })
            tables.append(table_data)
    return tables