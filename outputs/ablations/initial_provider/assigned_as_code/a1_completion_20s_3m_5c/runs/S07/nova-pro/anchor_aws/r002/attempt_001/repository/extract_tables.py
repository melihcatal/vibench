import boto3


def extract_tables(payload, config=None):
    config = config or {}
    client = boto3.client("textract", region_name=config.get("region"))
    response = client.analyze_document(Document={'Bytes': payload['document_bytes']}, FeatureTypes=['TABLES'])
    tables = []
    for table in response['Blocks']:
        if table['BlockType'] == 'TABLE':
            table_cells = [cell for cell in response['Blocks'] if cell['BlockType'] == 'CELL' and cell['Relationships'][0]['Ids'][0] == table['Id']]
            table_data = {
                'rows': [],
                'columns': [],
            }
            for cell in table_cells:
                row_index = cell['RowIndex']
                col_index = cell['ColumnIndex']
                if row_index not in table_data['rows']:
                    table_data['rows'].append(row_index)
                if col_index not in table_data['columns']:
                    table_data['columns'].append(col_index)
            tables.append(table_data)
    return tables