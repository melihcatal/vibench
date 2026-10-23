import json
import os
import uuid
from datetime import datetime
from database_client import get_s3_client
from database_models import ExportArchiveRequest, ExportArchiveResponse


def record_export_archive(request: ExportArchiveRequest) -> ExportArchiveResponse:
    """
    Archive exported document snapshots or attachments in Amazon S3.
    """
    s3 = get_s3_client()

    try:
        bucket_name = request.bucket_name or os.environ.get(
            "S3_BUCKET", "document-exports"
        )

        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        s3_key = (
            f"exports/{request.document_id}/{timestamp}_{unique_id}.{request.format}"
        )

        if request.format == "json":
            content = json.dumps(request.document, indent=2)
            content_type = "application/json"
        else:
            content = str(request.document)
            content_type = "text/plain"

        s3.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=content.encode("utf-8"),
            ContentType=content_type,
            Metadata={
                "document_id": request.document_id,
                "export_timestamp": timestamp,
                "export_format": request.format,
            },
        )

        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"

        return ExportArchiveResponse(
            success=True,
            document_id=request.document_id,
            s3_key=s3_key,
            s3_url=s3_url,
            message=f"Document exported to S3: {s3_url}",
        )
    except Exception as e:
        return ExportArchiveResponse(
            success=False,
            document_id=request.document_id,
            error_message=str(e),
            message="Failed to export document to S3",
        )
