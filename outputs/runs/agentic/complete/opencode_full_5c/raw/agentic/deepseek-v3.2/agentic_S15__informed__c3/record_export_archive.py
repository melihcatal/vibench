import os
import json
import tempfile
from typing import Dict, Any, List
from datetime import datetime
import boto3
from botocore.exceptions import ClientError


def archive_exported_records(
    records: List[Dict[str, Any]], bucket_name: str, prefix: str = "exports"
) -> Dict[str, Any]:
    """
    Archive exported document snapshots in Amazon S3.

    Args:
        records: List of document records to archive
        bucket_name: S3 bucket name
        prefix: S3 key prefix for the archive

    Returns:
        dict: Archive results
    """
    try:
        # AWS S3 configuration
        aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

        if not aws_access_key or not aws_secret_key:
            raise ValueError(
                "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required"
            )

        # Initialize S3 client
        s3_client = boto3.client(
            "s3", aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key
        )

        # Create temporary file for archive
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as temp_file:
            # Prepare metadata
            metadata = {
                "export_timestamp": datetime.utcnow().isoformat(),
                "record_count": len(records),
                "export_format": "json",
                "source": "document_store_export",
            }

            # Create archive structure
            archive_data = {"metadata": metadata, "records": records}

            # Write to temporary file
            json.dump(archive_data, temp_file, indent=2, default=str)
            temp_file_path = temp_file.name

        try:
            # Generate S3 key
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            s3_key = f"{prefix}/document_export_{timestamp}.json"

            # Upload to S3
            s3_client.upload_file(
                temp_file_path,
                bucket_name,
                s3_key,
                ExtraArgs={
                    "ContentType": "application/json",
                    "Metadata": {
                        "record-count": str(len(records)),
                        "export-timestamp": metadata["export_timestamp"],
                    },
                },
            )

            # Generate presigned URL for access (valid for 7 days)
            presigned_url = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket_name, "Key": s3_key},
                ExpiresIn=604800,  # 7 days in seconds
            )

            # Get file size
            file_size = os.path.getsize(temp_file_path)

            return {
                "success": True,
                "archive_location": {
                    "bucket": bucket_name,
                    "key": s3_key,
                    "presigned_url": presigned_url,
                    "file_size_bytes": file_size,
                },
                "metadata": metadata,
                "provider": "Amazon S3",
                "service": "s3.amazonaws.com",
            }

        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)

    except ClientError as e:
        return {
            "success": False,
            "error": f"AWS S3 error: {str(e)}",
            "record_count": len(records) if "records" in locals() else 0,
            "provider": "Amazon S3",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "record_count": len(records) if "records" in locals() else 0,
            "provider": "Amazon S3",
        }
