import os
import boto3

S3_BUCKET = "example-bucket"


def record_export_archive(document):
    s3 = boto3.client("s3")
    s3.put_object(Bucket=S3_BUCKET, Key=document["id"], Body=document["name"].encode())


if __name__ == "__main__":
    example_document = {"id": "example-id", "name": "example", "value": 123}
    record_export_archive(example_document)
