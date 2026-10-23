import boto3
from storage_client import get_s3_client
from storage_models import ObjectMetadata


def perform_ocr_on_stored_document(bucket_name, object_key):
    """Run OCR on a PDF or scanned image stored in S3 using Amazon Textract.

    Retrieves the object via the S3 client from storage_client.get_s3_client(),
    then calls Textract AnalyzeDocument for printed text detection.
    """
    s3 = get_s3_client()
    # Ensure the bucket and key exist (basic validation)
    metadata: ObjectMetadata = s3.head_object(Bucket=bucket_name, Key=object_key)
    if "ContentType" not in metadata or not metadata["ContentType"].startswith(
        ("image/", "application/pdf")
    ):
        raise ValueError("Object is not an image or PDF suitable for OCR")

    textract = boto3.client("textract")  # Uses credentials from environment
    response = textract.analyze_document(
        Document={"S3Object": {"Bucket": bucket_name, "Name": object_key}},
        FeatureTypes=["FORMS"],
    )
    return response  # Contains Blocks with recognized text and layout information
