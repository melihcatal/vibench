import boto3

def extract_tables(document_path):
    textract = boto3.client('textract')
    with open(document_path, 'rb') as document:
        imageBytes = document.read()
    response = textract.analyze_document(
        Document={'Bytes': imageBytes},
        FeatureTypes=['TABLES'])
    tables = []
    for block in response['Blocks']:
        if block['BlockType'] == 'TABLE':
            table = {
                'Id': block['Id'],
                'Rows': []
            }
            for relationship in block['Relationships']:
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        for block in response['Blocks']:
                            if block['Id'] == child_id:
                                if block['BlockType'] == 'CELL':
                                    cell = {
                                        'ColumnIndex': block.get('ColumnIndex', None),
                                        'RowIndex': block.get('RowIndex', None),
                                        'Text': block.get('Text', '')
                                    }
                                    table['Rows'].append(cell)
            tables.append(table)
    return tables

if __name__ == '__main__':
    document_path = 'path/to/your/document.pdf'
    tables = extract_tables(document_path)
    for table in tables:
        print(table)