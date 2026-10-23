import os
import boto3
from storage_models import StoredDocumentOcrRequest, StoredDocumentOcrResponse

def get_textract_client():
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set.")

    textract_client = boto3.client(
        "textract",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )
    return textract_client

def run_document_ocr(request: StoredDocumentOcrRequest) -> StoredDocumentOcrResponse:
    textract_client = get_textract_client()

    response = textract_client.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': request.bucket_name,
                'Name': request.object_name
            }
        }
    )

    text_content = []
    for item in response.get('Blocks', []):
        if item['BlockType'] == 'LINE':
            text_content.append(item['Text'])
    
    # Textract does not directly return detected languages in detect_document_text.
    # For a realistic scenario, one might use AWS Comprehend afterwards for language detection.
    # For this exercise, we will return a placeholder or infer from the context if possible.
    # As the task specifies concrete provider, I'll return an empty list for now.
    detected_languages = [] 

    return StoredDocumentOcrResponse(
        text_content="\n".join(text_content),
        detected_languages=detected_languages
    )
