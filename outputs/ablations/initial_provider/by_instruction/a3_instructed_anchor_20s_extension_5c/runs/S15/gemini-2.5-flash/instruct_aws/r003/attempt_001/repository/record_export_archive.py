import os
import json
from datetime import datetime
from database_client import get_s3_client

BUCKET_NAME = os.environ.get("S3_ARCHIVE_BUCKET_NAME", "your-s3-archive-bucket")

def archive_document_snapshot(document_id: str, document_content: dict, prefix: str = "document-snapshots/"):
    s3 = get_s3_client()

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"{prefix}{document_id}-{timestamp}.json"
    
    try:
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=json.dumps(document_content, indent=2),
            ContentType="application/json"
        )
        return {"status": "success", "archive_location": f"s3://{BUCKET_NAME}/{file_name}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def archive_attachment(document_id: str, attachment_name: str, attachment_content: bytes, content_type: str, prefix: str = "document-attachments/"):
    s3 = get_s3_client()

    file_name = f"{prefix}{document_id}/{attachment_name}"
    
    try:
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=attachment_content,
            ContentType=content_type
        )
        return {"status": "success", "archive_location": f"s3://{BUCKET_NAME}/{file_name}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
