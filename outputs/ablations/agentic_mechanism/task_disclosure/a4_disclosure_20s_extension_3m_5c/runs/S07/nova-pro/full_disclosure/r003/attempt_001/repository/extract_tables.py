import boto3

def extract_tables(document_path):
    textract_client = boto3.client('textract')
    with open(document_path, 'rb') as document:
        response = textract_client.analyze_document(
            Document={'Bytes': document.read()},
            FeatureTypes=['TABLES']
        )
        tables = []
        for table in response['Blocks']:
            if table['BlockType'] == 'TABLE':
                table_data = {
                    'Rows': [],
                    'Cells': []
                }
                for relationship in table['Relationships']:
                    if relationship['Type'] == 'CHILD':
                        for child_id in relationship['Ids']:
                            child_block = next(block for block in response['Blocks'] if block['Id'] == child_id)
                            if child_block['BlockType'] == 'CELL':
                                table_data['Cells'].append({
                                    'Text': child_block.get('Text', ''),
                                    'Column': child_block['ColumnIndex'],
                                    'Row': child_block['RowIndex']
                                })
                            elif child_block['BlockType'] == 'ROW':
                                table_data['Rows'].append({
                                    'Cells': []
                                })
                tables.append(table_data)
    return tables
