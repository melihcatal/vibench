import boto3


def record_export_archive(document, config):
    s3 = boto3.client("s3")
    bucket_name = config["bucket_name"]
    key = config["key_prefix"] + document[config["key_field"]]
    s3.put_object(Bucket=bucket_name, Key=key, Body=json.dumps(document))