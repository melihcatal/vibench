import boto3

def extract_tables(document_path):
    textract = boto3.client('textract')
    with open(document_path, 'rb') as document:
        response = textract.analyze_document(
            Document={'Bytes': document.read()},
            FeatureTypes=['TABLES'])
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
                        child_block = next(block for block in response['Blocks'] if block['Id'] == child_id)
                        if child_block['BlockType'] == 'CELL':
                            row_index = child_block['RowIndex']
                            column_index = child_block['ColumnIndex']
                            cell_text = child_block['Text']
                            if len(table_data['Rows']) <= row_index:
                                table_data['Rows'].append([])
                            if len(table_data['Columns']) <= column_index:
                                table_data['Columns'].append([])
                            table_data['Rows'][row_index-1].append(cell_text)
                            table_data['Columns'][column_index-1].append(cell_text)
            tables.append(table_data)
    return tables

if __name__ == '__main__':
    document_path = 'sample_document.pdf'
    tables = extract_tables(document_path)
    for table in tables:
        print(table)