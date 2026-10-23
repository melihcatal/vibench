import boto3

s3 = boto3.client('s3')
textract = boto3.client('textract')

def extract_key_values(bucket, document):
    response = textract.analyze_document(
        Document={'S3Object':{'Bucket':bucket,'Name':document}},
        FeatureTypes=['FORMS']
    )
    key_values = {}
    for item in response['Blocks']:
        if item['BlockType'] == 'KEY_VALUE_SET':
            key_values[item['Key']] = item['Value']
    return key_values