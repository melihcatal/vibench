import boto3

def export_archive(bucket_name, key, file_path):
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket_name, key)

if __name__ == '__main__':
    export_archive('my-bucket', 'my-key', 'my-file.txt')