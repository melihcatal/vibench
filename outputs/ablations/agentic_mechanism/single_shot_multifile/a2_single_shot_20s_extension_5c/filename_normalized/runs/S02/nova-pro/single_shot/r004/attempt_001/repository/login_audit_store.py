import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def store_audit_record(bucket_name, object_key, audit_record):
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=bucket_name, Key=object_key, Body=audit_record)
        print('Audit record stored successfully')
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f'AWS credentials error: {e}')
    except Exception as e:
        print(f'Error storing audit record: {e}')

if __name__ == '__main__':
    store_audit_record('your-bucket-name', 'your-object-key', 'your-audit-record')