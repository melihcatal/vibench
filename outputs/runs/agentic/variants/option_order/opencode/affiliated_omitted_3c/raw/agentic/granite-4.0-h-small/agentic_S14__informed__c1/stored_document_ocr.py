import boto3
import os
from .storage_client import StorageClient
from .storage_models import ObjectMetadata


class StoredDocumentOCR:
    """Run Amazon Textract OCR on a stored object in S3."""

    @classmethod
    def run(cls, bucket_name: str, key: str) -> Dict:
        # Download the object locally as a temporary file
        tmp_path = f"/tmp/{os.path.basename(key)}"
        StorageClient.s3.download_file(bucket_name, key, tmp_path)
        # Use Textract to analyze the file
        textract = boto3.client(
            "textract",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
        response = textract.analyze_document(
            Document={"S3Object": {"Bucket": bucket_name, "Name": key}},
            FeatureTypes=["FORMS"],  # or ["TABLES","FORMS"] as needed
        )
        # Clean up the temporary file
        os.remove(tmp_path)
        # Return a concise extraction of detected form fields
        fields = {}
        for block in response.get("Blocks", []):
            if block["BlockType"] == "KEY_VALUE_SET":
                key_block = next(
                    (b for b in response["Blocks"] if b["Id"] == block["KeyId"]), None
                )
                value_block = next(
                    (b for b in response["Blocks"] if b["Id"] == block["ValueId"]), None
                )
                if key_block and value_block:
                    fields[key_block["Text"]] = value_block["Text"]
        return {
            "status": "ocr_completed",
            "bucket": bucket_name,
            "key": key,
            "detected_fields": fields,
        }
