import boto3

def archive_document(bucket_name, document_id, file_path):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(file_path, bucket_name, document_id)
        print(f'Document {document_id} archived successfully.')
    except Exception as e:
        print(f'Error archiving document {document_id}: {e}')

# Example usage:
# archive_document('my-document-bucket', 'document123', 'path/to/document.pdf')