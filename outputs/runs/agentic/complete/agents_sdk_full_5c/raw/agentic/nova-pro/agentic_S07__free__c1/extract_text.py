import boto3

s3 = boto3.client('s3')
textract = boto3.client('textract')

def extract_text(bucket, document):
    response = textract.analyze_document(
        Document={'S3Object':{'Bucket':bucket,'Name':document}},
        FeatureTypes=['TABLES','FORMS']
    )
    text = ''
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            text += item['Text'] + ' '
    return text