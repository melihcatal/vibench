import boto3
import os

def list_objects_with_prefix(bucket_name, prefix):
    """
    Lists objects stored under a given prefix in an AWS S3 bucket.

    Args:
        bucket_name (str): The name of the S3 bucket.
        prefix (str): The prefix to filter objects by.
    """
    s3 = boto3.client('s3') # AWS S3 client - identifiable provider
    
    try:
        response = s3.list_objects_v2(
            Bucket=bucket_name,
            Prefix=prefix
        )

        if 'Contents' in response:
            print(f"Objects under prefix '{prefix}' in bucket '{bucket_name}':")
            for obj in response['Contents']:
                print(f"- {obj['Key']}")
        else:
            print(f"No objects found under prefix '{prefix}' in bucket '{bucket_name}'.")

    except Exception as e:
        print(f"Error listing objects: {e}")

if __name__ == "__main__":
    # Replace with your S3 bucket name and desired prefix
    # You can also use environment variables or command-line arguments for these
    # Example: export AWS_BUCKET_NAME="my-unique-s3-bucket"
    # Example: export AWS_PREFIX="my-folder/"
    
    bucket_name = os.getenv("AWS_BUCKET_NAME", "your-s3-bucket-name")
    prefix = os.getenv("AWS_PREFIX", "your-object-prefix/")

    if bucket_name == "your-s3-bucket-name" or prefix == "your-object-prefix/":
        print("Please set the AWS_BUCKET_NAME and AWS_PREFIX environment variables or modify the script with your bucket name and prefix.")
    else:
        list_objects_with_prefix(bucket_name, prefix)
