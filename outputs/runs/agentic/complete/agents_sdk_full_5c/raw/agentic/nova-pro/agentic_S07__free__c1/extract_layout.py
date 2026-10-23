import boto3

s3 = boto3.client('s3')
textract = boto3.client('textract')

def extract_layout(bucket, document):
    response = textract.analyze_document(
        Document={'S3Object':{'Bucket':bucket,'Name':document}},
        FeatureTypes=['TABLES','FORMS']
    )
    layout = []
    for item in response['Blocks']:
        if item['BlockType'] in ['LINE','WORD']:
            layout.append((item['BlockType'], item['Text'], item['Geometry']))
    return layout