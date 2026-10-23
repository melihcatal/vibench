import os
from storage_client import get_textract_client


def start_document_ocr(payload, config=None):
    config = config or {}
    bucket_name = config.get("bucket", os.environ.get("AWS_S3_BUCKET_NAME"))
    object_name = payload["object_name"]
    feature_types = payload.get("feature_types", ["FORMS", "TABLES"]) # Default to FORMS and TABLES

    textract_client = get_textract_client(config.get("region"))

    try:
        response = textract_client.start_document_analysis(
            DocumentLocation={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': object_name
                }
            },
            FeatureTypes=feature_types
        )
        return {"job_id": response["JobId"]}
    except Exception as e:
        raise RuntimeError(f"Error starting Textract document analysis: {e}")
