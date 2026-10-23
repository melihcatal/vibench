import boto3

def archive_record(record, bucket_name):
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket_name, Key=record['id'], Body=record['content'].encode('utf-8'))
    return {'archived': True}