import boto3
import os

def upload_object(bucket_name, object_name, file_path=None, data=None):
    """Uploads a file or byte stream to an S3 bucket.

    :param bucket_name: Name of the S3 bucket
    :param object_name: S3 object name. If using file_path, this will be the name of the file in S3.
    :param file_path: Path to the file to upload (optional)
    :param data: Byte stream to upload (optional)
    :return: True if object was uploaded, else False
    """
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION")
    )

    try:
        if file_path:
            s3_client.upload_file(file_path, bucket_name, object_name)
            print(f"File {file_path} uploaded to {bucket_name}/{object_name}")
        elif data is not None:
            s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=data)
            print(f"Byte stream uploaded to {bucket_name}/{object_name}")
        else:
            print("Either file_path or data must be provided.")
            return False
    except Exception as e:
        print(f"Error uploading object: {e}")
        return False
    return True

if __name__ == '__main__':
    # Example Usage:
    # Set your AWS credentials as environment variables:
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION

    # To upload a file:
    # with open("my_local_file.txt", "w") as f:
    #     f.write("This is a test file.")
    # upload_object("your-s3-bucket-name", "remote_file.txt", file_path="my_local_file.txt")

    # To upload a byte stream:
    # byte_data = b"This is a byte stream content."
    # upload_object("your-s3-bucket-name", "remote_byte_stream.txt", data=byte_data)
