import boto3
from storage_client import get_s3_client


def stored_document_ocr(bucket_name: str, object_name: str) -> dict:
    s3_client = get_s3_client(region="us-east-1")
    obj_response = s3_client.get_object(Bucket=bucket_name, Key=object_name)
    document = {"Bytes": obj_response["Body"].read()}
    textract_client = boto3.client("textract", region_name="us-east-1")
    response = textract_client.analyze_document(
        Document=document, FeatureTypes=["LAYOUT"]
    )
    return response
