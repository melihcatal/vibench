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
    for table in response['Blocks']:
        if table['BlockType'] == 'TABLE':
            table_data = {
                'Rows': [],
                'Columns': []
            }
            for relationship in table['Relationships']:
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        for block in response['Blocks']:
                            if block['Id'] == child_id:
                                if block['BlockType'] == 'CELL':
                                    row_index = block['RowIndex']
                                    col_index = block['ColumnIndex']
                                    cell_text = block['Text']
                                    if len(table_data['Rows']) < row_index:
                                        table_data['Rows'].append([])
                                    table_data['Rows'][row_index - 1].append(cell_text)
                                    if len(table_data['Columns']) < col_index:
                                        table_data['Columns'].append([])
                                    table_data['Columns'][col_index - 1].append(cell_text)
            tables.append(table_data)
    return tables