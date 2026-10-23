import boto3

# Set up client
s3 = boto3.client("s3")


# Function to archive metric snapshots
def archive_metric_snapshots(bucket_name, object_key, file_path):
    s3.upload_file(file_path, bucket_name, object_key)
