import boto3

def extract_tables(document_path):
    textract_client = boto3.client('textract')
    with open(document_path, 'rb') as document:
        document_bytes = document.read()
    response = textract_client.analyze_document(
        Document={'Bytes': document_bytes},
        FeatureTypes=['TABLES'])
    tables = []
    for table in response['Blocks']:
        if table['BlockType'] == 'TABLE':
            table_cells = []
            for relationship in table['Relationships']:
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        for block in response['Blocks']:
                            if block['Id'] == child_id:
                                if block['BlockType'] == 'CELL':
                                    table_cells.append(block['Text'])
            tables.append(table_cells)
    return tables

if __name__ == '__main__':
    document_path = 'sample_document.pdf'
    tables = extract_tables(document_path)
    for table in tables:
        print(table)