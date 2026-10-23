import boto3

s3 = boto3.client("s3")

bucket_name = "managed-object-storage"


def export_archive(document):
    s3.put_object(Bucket=bucket_name, Key=document["id"], Body=document["data"])
