import boto3

def upload_to_s3(file_path, bucket_name, object_name=None):
    s3_client = boto3.client('s3')
    if object_name is None:
        object_name = file_path
    try:
        response = s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"Upload successful: {file_path} -> {bucket_name}/{object_name}")
    except Exception as e:
        print(f"Error uploading file: {e}")

if __name__ == "__main__":
    file_path = 'metric_snapshot.csv'
    bucket_name = 'metrics-export-archive'
    upload_to_s3(file_path, bucket_name)