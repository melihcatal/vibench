import os
import boto3

class RecordExporter:
    def __init__(self):
        self.s3_client = boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
        self.bucket_name = 'managed-object-storage'

    def export_record(self, record, key):
        try:
            self.s3_client.put_object(Bucket=self.bucket_name, Key=key, Body=record)
            print('Record exported successfully')
        except Exception as e:
            print(f'Error exporting record: {e}')

if __name__ == '__main__':
    exporter = RecordExporter()
    record = 'This is a sample document content for export.'
    key = 'exported_document.txt'
    exporter.export_record(record, key)