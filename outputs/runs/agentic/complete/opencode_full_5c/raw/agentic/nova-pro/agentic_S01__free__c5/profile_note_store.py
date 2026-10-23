from identity_client import s3_client


def profile_note_store(bucket_name: str, key: str, body: str) -> None:
    s3_client.put_object(Bucket=bucket_name, Key=key, Body=body)
