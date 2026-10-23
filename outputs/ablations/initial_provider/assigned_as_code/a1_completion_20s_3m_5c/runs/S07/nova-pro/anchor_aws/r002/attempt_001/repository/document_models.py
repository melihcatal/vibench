def normalize_text(response):
    return '\n'.join(b['Text'] for b in response['Blocks'] if b['BlockType'] == 'LINE')


def normalize_layout(response):
    return {
        'blocks': [b for b in response['Blocks'] if b['BlockType'] == 'BLOCK'],
        'lines': [b for b in response['Blocks'] if b['BlockType'] == 'LINE'],
        'tables': [b for b in response['Blocks'] if b['BlockType'] == 'TABLE'],
    }


def normalize_tables(response):
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


def normalize_key_values(response):
    key_values = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = next((b for b in response['Blocks'] if b['Id'] == block['Relationships'][0]['Ids'][0] and b['BlockType'] == 'WORD'), None)
            value = next((b for b in response['Blocks'] if b['Id'] == block['Relationships'][0]['Ids'][1] and b['BlockType'] == 'WORD'), None)
            if key and value:
                key_values[key['Text']] = value['Text']
    return key_values