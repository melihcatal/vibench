import boto3

def stored_document_ocr(payload: dict, config: dict = None) -> dict:
    config = config or {}
    s3_bucket = config['s3_bucket']
    document_key = payload['object_name']

    client = boto3.client('textract', region_name=config.get('aws_region'))

    response = client.analyze_document(
        Document={
            'S3Object': {
                'Bucket': s3_bucket,
                'Name': document_key
            }
        },
        FeatureTypes=['FORMS', 'TABLES']
    )

    return {
        'object_name': document_key,
        'ocr_result': response
    }
