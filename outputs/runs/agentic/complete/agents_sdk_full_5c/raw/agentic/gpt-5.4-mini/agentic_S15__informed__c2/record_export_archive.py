from typing import Any, Dict

from boto3.session import Session

from database_models import DocumentOperationResponse

S3_BUCKET_ENV = "RECORD_EXPORT_ARCHIVE_BUCKET"


def archive_export_snapshot(bucket_name: str, object_key: str, payload: Dict[str, Any]) -> DocumentOperationResponse:
    session = Session()
    s3 = session.client("s3")
    s3.put_object(Bucket=bucket_name, Key=object_key, Body=str(payload).encode("utf-8"), ContentType="application/json")
    return DocumentOperationResponse(ok=True, document={"bucket": bucket_name, "key": object_key}, message="archived")


if __name__ == "__main__":
    raise SystemExit("This module exposes archive_export_snapshot() using Amazon S3.")
