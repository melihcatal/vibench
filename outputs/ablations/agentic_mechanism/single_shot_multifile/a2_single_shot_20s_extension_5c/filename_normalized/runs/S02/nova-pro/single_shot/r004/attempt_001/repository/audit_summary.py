import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def summarize_audit_events(bucket_name, object_key):
    s3 = boto3.client('s3')
    try:
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        audit_data = response['Body'].read().decode('utf-8')
        # Perform summarization logic here
        print('Audit summary generated')
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f'AWS credentials error: {e}')
    except Exception as e:
        print(f'Error summarizing audit events: {e}')

if __name__ == '__main__':
    summarize_audit_events('your-bucket-name', 'your-object-key')