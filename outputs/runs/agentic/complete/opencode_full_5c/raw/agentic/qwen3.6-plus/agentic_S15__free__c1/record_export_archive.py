import os
import json
from datetime import datetime, timezone
import boto3
from botocore.exceptions import ClientError
from database_models import ExportArchiveRequest, ExportArchiveResponse

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
S3_ARCHIVE_BUCKET = os.environ.get("S3_ARCHIVE_BUCKET", "document-archive-store")


def _get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_DEFAULT_REGION,
    )


def archive_record(request: ExportArchiveRequest) -> ExportArchiveResponse:
    s3_client = _get_s3_client()
    bucket = request.archive_bucket or S3_ARCHIVE_BUCKET
    key = request.to_s3_key()

    archive_payload = {
        "document_id": request.document_id,
        "data": request.data,
        "archived_at": datetime.now(timezone.utc).isoformat(),
        "metadata": request.metadata or {},
    }

    try:
        s3_client.put_object(
            Bucket=bucket,
            Key=key,
            Body=json.dumps(archive_payload, indent=2, default=str).encode("utf-8"),
            ContentType="application/json",
            StorageClass="STANDARD_IA",
        )

        archive_url = f"https://{bucket}.s3.{AWS_DEFAULT_REGION}.amazonaws.com/{key}"

        return ExportArchiveResponse(
            document_id=request.document_id,
            archive_key=key,
            archive_bucket=bucket,
            archive_url=archive_url,
            archived=True,
        )
    except ClientError as e:
        return ExportArchiveResponse(
            document_id=request.document_id,
            archive_key=key,
            archive_bucket=bucket,
            archived=False,
        )


def archive_record_raw(
    document_id: str,
    data: dict,
    archive_bucket: str = None,
    archive_key_prefix: str = "document-archives",
    metadata: dict = None,
) -> dict:
    request = ExportArchiveRequest(
        document_id=document_id,
        data=data,
        archive_bucket=archive_bucket,
        archive_key_prefix=archive_key_prefix,
        metadata=metadata,
    )
    response = archive_record(request)
    return response.to_dict()


if __name__ == "__main__":
    result = archive_record_raw(
        document_id="doc-004",
        data={"title": "Archived Report", "status": "completed", "final": True},
        archive_key_prefix="document-archives",
    )
    print(json.dumps(result, indent=2))
