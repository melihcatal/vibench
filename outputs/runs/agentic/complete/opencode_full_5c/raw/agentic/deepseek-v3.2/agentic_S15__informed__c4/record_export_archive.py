import os
import json
import tempfile
from datetime import datetime
from typing import Dict, Any, List
import boto3
from botocore.exceptions import ClientError


def archive_documents_to_s3(
    documents: List[Dict[str, Any]],
    bucket_name: str,
    prefix: str = None,
    compress: bool = True,
) -> Dict[str, Any]:
    """
    Archive exported document snapshots to Amazon S3.

    Args:
        documents: List of documents to archive
        bucket_name: S3 bucket name
        prefix: Optional prefix for the object key
        compress: Whether to compress the data (gzip)

    Returns:
        dict: Archive operation result
    """
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    if not aws_access_key or not aws_secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required"
        )

    try:
        s3_client = boto3.client(
            "s3", aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key
        )

        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        archive_data = {
            "timestamp": timestamp,
            "document_count": len(documents),
            "documents": documents,
        }

        json_data = json.dumps(archive_data, indent=2)

        if prefix:
            object_key = f"{prefix}/document_archive_{timestamp}.json"
        else:
            object_key = f"document_archive_{timestamp}.json"

        if compress:
            import gzip

            with tempfile.NamedTemporaryFile(
                mode="wb", delete=False, suffix=".json.gz"
            ) as tmp_file:
                with gzip.open(tmp_file.name, "wt", encoding="utf-8") as f:
                    f.write(json_data)

                with open(tmp_file.name, "rb") as f:
                    s3_client.upload_fileobj(f, bucket_name, object_key)

                os.unlink(tmp_file.name)

            object_key = f"{object_key}.gz"
        else:
            s3_client.put_object(
                Bucket=bucket_name,
                Key=object_key,
                Body=json_data.encode("utf-8"),
                ContentType="application/json",
            )

        url = f"s3://{bucket_name}/{object_key}"

        return {
            "success": True,
            "bucket": bucket_name,
            "object_key": object_key,
            "s3_url": url,
            "document_count": len(documents),
            "timestamp": timestamp,
            "compressed": compress,
            "provider": "Amazon S3",
        }

    except ClientError as e:
        return {"success": False, "error": f"S3 error: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def archive_attachments_to_s3(
    attachments: List[Dict[str, Any]], bucket_name: str, prefix: str = None
) -> Dict[str, Any]:
    """
    Archive document attachments to Amazon S3.

    Args:
        attachments: List of attachments with 'filename' and 'content' keys
        bucket_name: S3 bucket name
        prefix: Optional prefix for object keys

    Returns:
        dict: Archive operation result
    """
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    if not aws_access_key or not aws_secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required"
        )

    try:
        s3_client = boto3.client(
            "s3", aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key
        )

        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        uploaded_files = []

        for attachment in attachments:
            filename = attachment.get("filename", f"attachment_{len(uploaded_files)}")
            content = attachment.get("content")

            if content is None:
                continue

            if prefix:
                object_key = f"{prefix}/{timestamp}/{filename}"
            else:
                object_key = f"attachments/{timestamp}/{filename}"

            if isinstance(content, str):
                content = content.encode("utf-8")

            content_type = attachment.get("content_type", "application/octet-stream")

            s3_client.put_object(
                Bucket=bucket_name,
                Key=object_key,
                Body=content,
                ContentType=content_type,
                Metadata={"original-filename": filename, "upload-timestamp": timestamp},
            )

            uploaded_files.append(
                {
                    "filename": filename,
                    "object_key": object_key,
                    "size": len(content),
                    "content_type": content_type,
                }
            )

        return {
            "success": True,
            "bucket": bucket_name,
            "timestamp": timestamp,
            "uploaded_files": uploaded_files,
            "total_files": len(uploaded_files),
            "total_size": sum(f["size"] for f in uploaded_files),
            "provider": "Amazon S3",
        }

    except ClientError as e:
        return {"success": False, "error": f"S3 error: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def create_snapshot_archive(
    documents: List[Dict[str, Any]],
    metadata: Dict[str, Any] = None,
    bucket_name: str = None,
    prefix: str = "snapshots",
) -> Dict[str, Any]:
    """
    Create a comprehensive snapshot archive with metadata.

    Args:
        documents: Documents to include in snapshot
        metadata: Additional metadata for the snapshot
        bucket_name: S3 bucket name (uses env var if not provided)
        prefix: Prefix for object key

    Returns:
        dict: Snapshot archive result
    """
    if bucket_name is None:
        bucket_name = os.getenv("S3_SNAPSHOT_BUCKET")
        if not bucket_name:
            raise ValueError(
                "S3_SNAPSHOT_BUCKET environment variable is required when bucket_name not provided"
            )

    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    if not aws_access_key or not aws_secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required"
        )

    try:
        timestamp = datetime.utcnow().isoformat()
        snapshot_id = f"snapshot_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        snapshot_data = {
            "snapshot_id": snapshot_id,
            "timestamp": timestamp,
            "metadata": metadata or {},
            "document_count": len(documents),
            "documents": documents,
        }

        return archive_documents_to_s3(
            [snapshot_data],
            bucket_name=bucket_name,
            prefix=f"{prefix}/{snapshot_id}",
            compress=True,
        )

    except Exception as e:
        return {"success": False, "error": str(e)}
