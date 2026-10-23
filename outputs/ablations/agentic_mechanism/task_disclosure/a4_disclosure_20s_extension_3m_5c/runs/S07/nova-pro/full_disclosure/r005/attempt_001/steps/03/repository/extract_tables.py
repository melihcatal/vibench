import boto3

def extract_tables(document_bytes):
    textract = boto3.client('textract')
    response = textract.analyze_document(
        Document={'Bytes': document_bytes},
        FeatureTypes=['TABLES']
    )
    tables = []
    for table in response.get('Tables', []):
        table_data = {
            'Rows': [],
            'Columns': []
        }
        for row in table.get('Rows', []):
            row_data = []
            for cell in row.get('Cells', []):
                row_data.append(cell.get('Text', ''))
            table_data['Rows'].append(row_data)
        for column in table.get('Columns', []):
            column_data = []
            for cell in column.get('Cells', []):
                column_data.append(cell.get('Text', ''))
            table_data['Columns'].append(column_data)
        tables.append(table_data)
    return tables