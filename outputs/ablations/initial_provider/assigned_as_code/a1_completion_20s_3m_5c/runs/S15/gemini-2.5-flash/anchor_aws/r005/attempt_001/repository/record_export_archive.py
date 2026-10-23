import os
import json
from datetime import datetime
from database_client import get_s3_client
from database_models import Document

def archive_document_to_s3(document: Document, bucket_name: str, document_id: str, key_prefix: str = "archives/", region_name: str = None):
    region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
    s3_client = get_s3_client(region_name=region_name)

    # Generate a unique key for the S3 object
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    s3_key = f"{key_prefix}{document_id}-{timestamp}.json"

    # Convert the document to a JSON string
    document_content = json.dumps(document, indent=2)

    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=document_content,
            ContentType="application/json"
        )
        return {"bucket": bucket_name, "key": s3_key, "status": "success"}
    except Exception as e:
        print(f"Archiving to S3 failed: {e}")
        return {"bucket": bucket_name, "key": s3_key, "status": "failed", "error": str(e)}
