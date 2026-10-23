import boto3
from botocore.exceptions import ClientError

def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: String
    :param object_name: String
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Replace with your AWS credentials and region
    # It's recommended to use environment variables or IAM roles for production
    aws_access_key_id = "YOUR_AWS_ACCESS_KEY_ID"
    aws_secret_access_key = "YOUR_AWS_SECRET_ACCESS_KEY"
    aws_region = "YOUR_AWS_REGION" # e.g., "us-east-1"

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )
    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )
    except ClientError as e:
        print(e)
        return None

    # The response contains the presigned URL
    return response

if __name__ == "__main__":
    # Example usage:
    bucket = "YOUR_S3_BUCKET_NAME"
    object = "YOUR_S3_OBJECT_KEY" # e.g., "myfolder/myfile.txt"

    if "YOUR_S3_BUCKET_NAME" in bucket or "YOUR_S3_OBJECT_KEY" in object:
        print("Please replace 'YOUR_S3_BUCKET_NAME' and 'YOUR_S3_OBJECT_KEY' with your actual S3 bucket and object key.")
        print("Also, replace 'YOUR_AWS_ACCESS_KEY_ID', 'YOUR_AWS_SECRET_ACCESS_KEY', and 'YOUR_AWS_REGION' with your AWS credentials and region.")
    else:
        url = create_presigned_url(bucket, object)
        if url:
            print(f"Presigned URL: {url}")
        else:
            print("Could not generate presigned URL.")
