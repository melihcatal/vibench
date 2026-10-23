import boto3


def extract_tables(payload, config=None):
    config = config or {}
    client = boto3.client("textract", region_name=config.get("region"))
    response = client.analyze_document(Document={'Bytes': payload['document_bytes']}, FeatureTypes=['TABLES'])
    tables = []
    for table in response['Blocks']:
        if table['BlockType'] == 'TABLE':
            table_data = {
                'id': table['Id'],
                'cells': []
            }
            for relationship in table['Relationships']:
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        for block in response['Blocks']:
                            if block['Id'] == child_id:
                                table_data['cells'].append(block['Text'])
            tables.append(table_data)
    return tables