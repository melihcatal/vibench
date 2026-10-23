import boto3
import textract


def run_ocr_on_stored_document(object_name, config=None):
    config = config or {}
    client = boto3.client('s3', region_name=config.get('region'))
    response = client.get_object(Bucket=config['bucket'], Key=object_name)
    document_content = response['Body'].read()
    text = textract.process(document_content, method='tesseract')
    return text.decode('utf-8')