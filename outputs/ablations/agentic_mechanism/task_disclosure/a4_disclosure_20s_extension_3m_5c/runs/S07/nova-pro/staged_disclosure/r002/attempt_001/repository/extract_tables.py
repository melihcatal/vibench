import boto3

def extract_tables(document):
    client = boto3.client('textract')
    response = client.analyze_document(
        Document={'Bytes': document},
        FeatureTypes=['TABLES'])
    tables = []
    for table in response['Blocks']:
        if table['BlockType'] == 'TABLE':
            rows = []
            for relationship in table['Relationships']:
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        child_block = next(block for block in response['Blocks'] if block['Id'] == child_id)
                        if child_block['BlockType'] == 'CELL':
                            rows.append(child_block['Text'])
            tables.append(rows)
    return tables