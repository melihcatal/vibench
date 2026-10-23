import os
import json
from typing import Dict, Any
from database_client import get_s3_client

def archive_document_snapshot(bucket_name: str, object_key: str, document_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Archives exported document snapshots or attachments in managed object storage (AWS S3).
    
    Args:
        bucket_name: The name of the S3 bucket.
        object_key: The key (path) for the object in the S3 bucket (e.g., 'exports/document-123.json').
        document_data: The JSON document data to archive.
        
    Returns:
        The response from the S3 put_object operation.
    """
    s3 = get_s3_client()
    
    # Convert document data to a JSON string
    file_content = json.dumps(document_data, indent=2)
    
    response = s3.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=file_content,
        ContentType='application/json'
    )
    return response

if __name__ == "__main__":
    # Example Usage (requires AWS credentials and S3 bucket configured)
    s3_bucket_name = os.getenv("S3_ARCHIVE_BUCKET_NAME", "your-archive-bucket")
    
    sample_document_to_archive = {
        "id": "doc456",
        "version": 5,
        "status": "archived",
        "exported_at": "2023-10-27T10:00:00Z",
        "content_snapshot": "This is a snapshot of the document content at the time of export."
    }
    object_key_name = f"exports/document-{sample_document_to_archive['id']}.json"
    
    print(f"Archiving document snapshot to S3 bucket '{s3_bucket_name}' with key '{object_key_name}'...")
    try:
        response = archive_document_snapshot(s3_bucket_name, object_key_name, sample_document_to_archive)
        print("Document archived successfully:", json.dumps(response, indent=2))
    except Exception as e:
        print(f"Error archiving document: {e}")
