import boto3

S3_CLIENT = boto3.client('s3')
BUCKET_NAME = 'my-document-archive'


def archive_document_snapshot(document_id, snapshot_file_path):
    '''Upload a document snapshot/attachment to S3 for long‑term archival.'''
    try:
        S3_CLIENT.upload_file(snapshot_file_path, BUCKET_NAME, f'{document_id}/{snapshot_file_path}')
    except Exception as e:
        raise RuntimeError(f'Failed to archive snapshot: {e}')

# Example usage (local):
# archive_document_snapshot('doc-456', 'exports/doc-456.json')
