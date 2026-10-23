import boto3

def archive_document(bucket_name, document_key, document_content):
    s3_client = boto3.client('s3')
    s3_client.put_object(Bucket=bucket_name, Key=document_key, Body=document_content)
    print(f'Document archived to {bucket_name}/{document_key}')

# Example usage
# archive_document('my-bucket', 'document-key', 'document-content')