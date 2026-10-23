
import boto3
from botocore.exceptions import ClientError
import os

def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: String
    :param object_name: String
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Ensure AWS credentials are set as environment variables
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN (optional)
    # AWS_REGION (e.g., us-east-1)

    s3_client = boto3.client('s3',
                             aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                             aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
                             region_name=os.environ.get('AWS_REGION'))
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        print(f"Error generating presigned URL: {e}")
        return None
    return response

if __name__ == "__main__":
    # Replace with your S3 bucket and object details
    your_bucket_name = "your-s3-bucket-name"
    your_object_name = "your-object-key/file.txt" # e.g., "myfolder/document.pdf"

    # Set AWS environment variables (for demonstration purposes, in a real app use secure methods)
    # os.environ['AWS_ACCESS_KEY_ID'] = 'YOUR_AWS_ACCESS_KEY_ID'
    # os.environ['AWS_SECRET_ACCESS_KEY'] = 'YOUR_AWS_SECRET_ACCESS_KEY'
    # os.environ['AWS_REGION'] = 'us-east-1' # e.g., 'us-west-2'

    presigned_url = create_presigned_url(your_bucket_name, your_object_name)

    if presigned_url:
        print(f"Presigned URL for {your_object_name}:\n{presigned_url}")
        print("This URL is valid for 1 hour.")
    else:
        print("Failed to generate presigned URL.")
