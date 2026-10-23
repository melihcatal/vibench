import boto3
from storage_client import get_storage_client
from storage_models import ObjectMetadataRequest

def run_ocr_on_stored_document(bucket_name: str, object_key: str) -> dict:
    s3_client = get_storage_client()
    textract_client = boto3.client('textract', region_name='us-east-1')

    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        document_bytes = response['Body'].read()

        textract_response = textract_client.detect_document_text(
            Document={'Bytes': document_bytes}
        )
        extracted_text = " ".join([
            item["Text"] for item in textract_response["Blocks"] 
            if item["BlockType"] == "LINE"
        ])
        return {
            "bucket_name": bucket_name,
            "object_key": object_key,
            "extracted_text": extracted_text,
            "success": True
        }
    except Exception as e:
        return {
            "bucket_name": bucket_name,
            "object_key": object_key,
            "success": False,
            "error": str(e)
        }