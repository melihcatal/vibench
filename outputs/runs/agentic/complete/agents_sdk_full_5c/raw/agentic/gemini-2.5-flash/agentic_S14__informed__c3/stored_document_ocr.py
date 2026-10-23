import os
import boto3
from typing import Dict, Any, List

def run_ocr_on_stored_document(
    bucket_name: str,
    object_key: str,
    feature_types: List[str] = ['FORMS', 'TABLES']
) -> Dict[str, Any]:
    """
    Runs OCR and layout extraction on a document stored in S3 using Amazon Textract.

    Args:
        bucket_name: The name of the S3 bucket where the document is stored.
        object_key: The key (path) of the document object in the S3 bucket.
        feature_types: A list of feature types to detect, e.g., 'FORMS', 'TABLES'.
                       Refer to Textract documentation for full list.

    Returns:
        A dictionary containing the raw response from Textract's analyze_document.
    """
    textract_client = boto3.client(
        'textract',
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )

    try:
        response = textract_client.analyze_document(
            Document={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': object_key
                }
            },
            FeatureTypes=feature_types
        )
        return response
    except Exception as e:
        print(f"Error running Textract OCR: {e}")
        raise
