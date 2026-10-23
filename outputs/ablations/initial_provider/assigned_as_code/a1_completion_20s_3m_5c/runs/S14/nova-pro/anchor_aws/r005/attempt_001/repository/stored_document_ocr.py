import boto3
from botocore.exceptions import NoCredentialsError


def ocr_stored_document(bucket_name, object_name):
    try:
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=bucket_name, Key=object_name)
        file_stream = response['Body']
        # Perform OCR on the file stream
        # This is a placeholder for the actual OCR implementation
        return "OCR result"
    except NoCredentialsError:
        return "Credentials not available"