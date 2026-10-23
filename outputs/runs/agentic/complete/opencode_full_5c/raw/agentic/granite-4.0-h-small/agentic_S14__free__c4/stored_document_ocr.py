import boto3
from storage_client import get_managed_storage_client
from storage_models import PutObjectRequest, HeadObjectResponse

# Example OCR provider: AWS Textract (managed OCR for documents)


def ocr_stored_document(bucket_name: str, object_key: str) -> dict:
    """Run OCR on a stored PDF/DOCX document using managed OCR service and return extracted text blocks."""
    client = get_managed_storage_client()
    # Download the document (using temporary presigned URL or direct client)
    # For simplicity, use S3 client to get object bytes directly
    response = client.get_object(Bucket=bucket_name, Key=object_key)
    document_bytes = response["Body"].read()

    # Call Textract to perform OCR (using same AWS credentials as storage client)
    textract = boto3.client("textract", region_name=boto3.Session().region_name)
    ocr_result = textract.analyze_document(
        Document={"Bytes": document_bytes},
        FeatureTypes=["FORMS", "TABLES"],  # detect forms and tables in PDFs
    )
    return ocr_result  # includes Blocks, Pages, etc.
