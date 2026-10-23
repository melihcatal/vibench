from s3_client import get_s3_client


def record_export_archive(document_id, document):
    client = get_s3_client()
    client.put_object(
        Bucket=S3_BUCKET_NAME, Key=f"{document_id}.json", Body=json.dumps(document)
    )
