import boto3
from document_client import get_textract_client

def extract_tables(document_path):
    textract_client = get_textract_client()
    with open(document_path, 'rb') as document:
        image_bytes = document.read()
    response = textract_client.analyze_document(Document={'Bytes': image_bytes}, FeatureTypes=['TABLES'])
    tables = []
    for table in response['Blocks']:
        if table['BlockType'] == 'TABLE':
            table_data = {
                'cells': [],
                'rows': []
            }
            for relationship in table['Relationships']:
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        for block in response['Blocks']:
                            if block['Id'] == child_id:
                                if block['BlockType'] == 'CELL':
                                    table_data['cells'].append(block['Text'])
                                elif block['BlockType'] == 'ROW':
                                    table_data['rows'].append(block['Text'])
            tables.append(table_data)
    return tables