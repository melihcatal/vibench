import boto3


def export_records_to_s3(records, bucket_name, prefix):
    s3 = boto3.client('s3')
    for i, record in enumerate(records):
        key = f"{prefix}/{i}.json"
        s3.put_object(Bucket=bucket_name, Key=key, Body=json.dumps(record))