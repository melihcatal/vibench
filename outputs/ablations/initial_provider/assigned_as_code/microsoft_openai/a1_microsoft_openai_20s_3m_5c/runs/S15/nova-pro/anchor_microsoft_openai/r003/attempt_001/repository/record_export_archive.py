import boto3

def export_records_to_s3(records, bucket_name):
    s3 = boto3.client('s3')
    for record in records:
        s3.put_object(Bucket=bucket_name, Key=record['id'], Body=str(record))