import boto3

s3 = boto3.client('s3')
textract = boto3.client('textract')

def extract_tables(bucket, document):
    response = textract.analyze_document(
        Document={'S3Object':{'Bucket':bucket,'Name':document}},
        FeatureTypes=['TABLES']
    )
    tables = []
    for item in response['Blocks']:
        if item['BlockType'] == 'TABLE':
            tables.append(item)
    return tables