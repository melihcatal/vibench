import os
import json
import zipfile
import tempfile
import boto3
from typing import List, Dict, Any
from botocore.exceptions import ClientError
from datetime import datetime
from database_models import ExportArchiveRequest, ExportArchiveResponse

# AWS S3 configuration
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "document-exports")
S3_PREFIX = os.environ.get("S3_PREFIX", "archives/")

# S3 client cache
_s3_client = None


def get_s3_client():
    """
    Get or create an AWS S3 client.
    """
    global _s3_client

    if _s3_client is None:
        client_kwargs = {"region_name": AWS_REGION}

        if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
            client_kwargs["aws_access_key_id"] = AWS_ACCESS_KEY_ID
            client_kwargs["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY

        _s3_client = boto3.client("s3", **client_kwargs)

    return _s3_client


def export_and_archive_records(request: ExportArchiveRequest) -> ExportArchiveResponse:
    """
    Archive exported document snapshots or attachments in AWS S3.
    """
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        return ExportArchiveResponse(
            success=False,
            archive_url=None,
            archive_key=None,
            document_count=0,
            error="AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required",
            timestamp=request.timestamp,
        )

    if not S3_BUCKET_NAME:
        return ExportArchiveResponse(
            success=False,
            archive_url=None,
            archive_key=None,
            document_count=0,
            error="S3_BUCKET_NAME environment variable is required",
            timestamp=request.timestamp,
        )

    try:
        s3 = get_s3_client()

        # Create a temporary directory for archive creation
        with tempfile.TemporaryDirectory() as temp_dir:
            archive_filename = (
                f"documents_export_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.zip"
            )
            archive_path = os.path.join(temp_dir, archive_filename)

            # Create ZIP archive
            with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                # Add each document as a JSON file
                for i, (doc_id, doc_data) in enumerate(
                    zip(request.document_ids, request.documents)
                ):
                    # Create document file content
                    doc_content = {
                        "id": doc_id,
                        "exported_at": request.timestamp
                        or datetime.utcnow().isoformat(),
                        "data": doc_data,
                    }

                    # Write document to JSON file in archive
                    doc_filename = f"document_{i + 1:03d}_{doc_id}.json"
                    zipf.writestr(doc_filename, json.dumps(doc_content, indent=2))

                    # Add attachments if requested
                    if request.include_attachments and "attachments" in doc_data:
                        attachments = doc_data.get("attachments", [])
                        for att_idx, attachment in enumerate(attachments):
                            if (
                                isinstance(attachment, dict)
                                and "filename" in attachment
                                and "content" in attachment
                            ):
                                att_filename = f"attachments/{doc_id}/attachment_{att_idx + 1:03d}_{attachment['filename']}"
                                # In real implementation, you'd handle binary content properly
                                # For this example, we assume text content
                                zipf.writestr(att_filename, str(attachment["content"]))

            # Get archive size
            archive_size = os.path.getsize(archive_path)

            # Determine S3 key
            if request.storage_path:
                s3_key = request.storage_path
            else:
                s3_key = f"{S3_PREFIX}{archive_filename}"

            # Upload to S3
            with open(archive_path, "rb") as archive_file:
                s3.upload_fileobj(
                    archive_file,
                    S3_BUCKET_NAME,
                    s3_key,
                    ExtraArgs={
                        "ContentType": "application/zip",
                        "Metadata": {
                            "document-count": str(len(request.document_ids)),
                            "export-timestamp": request.timestamp
                            or datetime.utcnow().isoformat(),
                        },
                    },
                )

            # Generate presigned URL for download (valid for 1 hour)
            archive_url = s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": S3_BUCKET_NAME, "Key": s3_key},
                ExpiresIn=3600,
            )

            return ExportArchiveResponse(
                success=True,
                archive_url=archive_url,
                archive_key=s3_key,
                document_count=len(request.document_ids),
                archive_size_bytes=archive_size,
                timestamp=request.timestamp,
            )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]
        return ExportArchiveResponse(
            success=False,
            archive_url=None,
            archive_key=None,
            document_count=0,
            error=f"AWS S3 {error_code}: {error_message}",
            timestamp=request.timestamp,
        )
    except Exception as e:
        return ExportArchiveResponse(
            success=False,
            archive_url=None,
            archive_key=None,
            document_count=0,
            error=f"Unexpected error: {str(e)}",
            timestamp=request.timestamp,
        )


# Alternative implementation for streaming archive creation
def create_streaming_archive(documents: List[Dict[str, Any]], output_stream):
    """
    Create a ZIP archive directly to an output stream.
    """
    with zipfile.ZipFile(output_stream, "w", zipfile.ZIP_DEFLATED) as zipf:
        for i, doc in enumerate(documents):
            doc_id = doc.get("id", f"doc_{i}")
            doc_filename = f"document_{i + 1:03d}_{doc_id}.json"
            zipf.writestr(doc_filename, json.dumps(doc, indent=2))


# Helper for exporting single document
def export_single_document(document_id: str, document_data: Dict[str, Any]) -> str:
    """
    Export a single document to S3 and return the URL.
    """
    request = ExportArchiveRequest(
        document_ids=[document_id], documents=[document_data], archive_format="zip"
    )

    response = export_and_archive_records(request)

    if response.success and response.archive_url:
        return response.archive_url
    else:
        raise Exception(f"Export failed: {response.error}")


# Batch export with custom naming
def batch_export_documents(
    documents: List[Dict[str, Any]],
    archive_name: str = None,
    metadata: Dict[str, str] = None,
) -> ExportArchiveResponse:
    """
    Export multiple documents with custom archive name and metadata.
    """
    document_ids = [doc.get("id", f"doc_{i}") for i, doc in enumerate(documents)]

    if not archive_name:
        archive_name = f"batch_export_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

    request = ExportArchiveRequest(
        document_ids=document_ids,
        documents=documents,
        storage_path=f"{S3_PREFIX}{archive_name}.zip",
    )

    return export_and_archive_records(request)


# List existing exports
def list_exports(prefix: str = None, max_results: int = 100) -> List[Dict[str, Any]]:
    """
    List existing export archives in S3.
    """
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        raise ValueError("AWS credentials required")

    try:
        s3 = get_s3_client()

        list_prefix = prefix or S3_PREFIX
        response = s3.list_objects_v2(
            Bucket=S3_BUCKET_NAME, Prefix=list_prefix, MaxKeys=max_results
        )

        exports = []
        if "Contents" in response:
            for obj in response["Contents"]:
                # Get object metadata
                head_response = s3.head_object(Bucket=S3_BUCKET_NAME, Key=obj["Key"])

                metadata = head_response.get("Metadata", {})

                exports.append(
                    {
                        "key": obj["Key"],
                        "size": obj["Size"],
                        "last_modified": obj["LastModified"].isoformat(),
                        "document_count": int(metadata.get("document-count", 0)),
                        "export_timestamp": metadata.get("export-timestamp"),
                    }
                )

        return exports

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]
        raise Exception(f"Failed to list exports: {error_code} - {error_message}")
    except Exception as e:
        raise Exception(f"Failed to list exports: {str(e)}")
