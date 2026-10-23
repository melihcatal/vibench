import os
import json
import tempfile
import zipfile
from datetime import datetime
from typing import Dict, Any, List
import io


def record_export_archive(
    documents: List[Dict[str, Any]],
    archive_name: str = None,
    format_type: str = "json",
    include_attachments: bool = False,
) -> Dict[str, Any]:
    """
    Archive exported document snapshots in AWS S3.

    Args:
        documents: List of document records to archive
        archive_name: Name for the archive (default: timestamp-based)
        format_type: Export format ("json", "csv", "both")
        include_attachments: Whether to include binary attachments

    Returns:
        dict: Archive creation result with S3 URL
    """
    try:
        import boto3
        from botocore.exceptions import ClientError

        # Initialize S3 client
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
        )

        bucket_name = os.environ.get("S3_BUCKET_NAME", "document-archives")

        # Generate archive name if not provided
        if not archive_name:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            archive_name = f"document_export_{timestamp}"

        # Create temporary directory for archive contents
        with tempfile.TemporaryDirectory() as temp_dir:
            archive_files = []

            # 1. Create JSON export
            if format_type in ["json", "both"]:
                json_data = {
                    "export_timestamp": datetime.utcnow().isoformat() + "Z",
                    "document_count": len(documents),
                    "documents": documents,
                    "export_format": "json",
                    "provider": "aws:dynamodb",
                }

                json_filename = f"{archive_name}.json"
                json_path = os.path.join(temp_dir, json_filename)

                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(json_data, f, indent=2, default=str)

                archive_files.append(json_filename)

            # 2. Create CSV export (simplified)
            if format_type in ["csv", "both"]:
                import csv

                # Extract field names from documents
                all_fields = set()
                for doc in documents:
                    doc_data = doc.get("data", {})
                    all_fields.update(doc_data.keys())

                # Create CSV file
                csv_filename = f"{archive_name}.csv"
                csv_path = os.path.join(temp_dir, csv_filename)

                with open(csv_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)

                    # Write header
                    header = ["document_id", "updated_at"] + sorted(all_fields)
                    writer.writerow(header)

                    # Write rows
                    for doc in documents:
                        doc_id = doc.get("id", "")
                        updated_at = doc.get("updated_at", "")
                        doc_data = doc.get("data", {})

                        row = [doc_id, updated_at]
                        for field in sorted(all_fields):
                            value = doc_data.get(field, "")
                            # Convert to string
                            if isinstance(value, (dict, list)):
                                value = json.dumps(value)
                            row.append(str(value))

                        writer.writerow(row)

                archive_files.append(csv_filename)

            # 3. Create metadata file
            metadata = {
                "archive_name": archive_name,
                "created_at": datetime.utcnow().isoformat() + "Z",
                "document_count": len(documents),
                "formats": format_type,
                "include_attachments": include_attachments,
                "provider": "aws:s3",
                "source_provider": "aws:dynamodb",
            }

            metadata_filename = "metadata.json"
            metadata_path = os.path.join(temp_dir, metadata_filename)

            with open(metadata_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2)

            archive_files.append(metadata_filename)

            # 4. Create ZIP archive in memory
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for filename in archive_files:
                    file_path = os.path.join(temp_dir, filename)
                    zip_file.write(file_path, filename)

            zip_buffer.seek(0)
            zip_size = len(zip_buffer.getvalue())

            # 5. Upload to S3
            s3_key = f"exports/{archive_name}.zip"

            s3_client.put_object(
                Bucket=bucket_name,
                Key=s3_key,
                Body=zip_buffer,
                ContentType="application/zip",
                Metadata={
                    "document-count": str(len(documents)),
                    "export-format": format_type,
                    "created-by": "document-export-service",
                },
            )

            # Generate S3 URL
            s3_url = f"https://{bucket_name}.s3.{os.environ.get('AWS_REGION', 'us-east-1')}.amazonaws.com/{s3_key}"

            # Generate pre-signed URL for temporary access
            presigned_url = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket_name, "Key": s3_key},
                ExpiresIn=3600,  # 1 hour
            )

            return {
                "success": True,
                "archive_name": archive_name,
                "s3_location": {
                    "bucket": bucket_name,
                    "key": s3_key,
                    "url": s3_url,
                    "presigned_url": presigned_url,
                },
                "archive_details": {
                    "file_count": len(archive_files),
                    "files": archive_files,
                    "size_bytes": zip_size,
                    "format": format_type,
                    "document_count": len(documents),
                },
                "metadata": metadata,
                "provider": "aws:s3",
            }

    except ImportError:
        return {
            "success": False,
            "error": "boto3 library not installed. Install with: pip install boto3",
            "provider": "aws:s3",
        }
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "NoSuchBucket":
            return {
                "success": False,
                "error": f"S3 bucket {bucket_name} does not exist",
                "provider": "aws:s3",
            }
        elif error_code == "AccessDenied":
            return {
                "success": False,
                "error": "Access denied to S3 bucket. Check AWS credentials and permissions.",
                "provider": "aws:s3",
            }
        return {
            "success": False,
            "error": f"AWS S3 error: {str(e)}",
            "provider": "aws:s3",
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "provider": "aws:s3",
        }
