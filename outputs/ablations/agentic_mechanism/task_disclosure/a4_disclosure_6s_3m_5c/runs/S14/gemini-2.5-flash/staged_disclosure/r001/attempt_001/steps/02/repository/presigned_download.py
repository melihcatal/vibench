import boto3
from botocore.exceptions import ClientError
import logging

def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: String
    :param object_name: String
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response

if __name__ == '__main__':
    # Replace with your S3 bucket name and object key
    # Ensure you have AWS credentials configured in your environment
    # (e.g., via AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN environment variables
    # or ~/.aws/credentials file)
    
    bucket = 'your-s3-bucket-name'
    key = 'your-object-key'
    
    # Example usage: Generate a presigned URL that expires in 1 hour (3600 seconds)
    presigned_url = create_presigned_url(bucket, key, 3600)
    if presigned_url:
        print(f"Presigned URL: {presigned_url}")
    else:
        print("Could not generate presigned URL.")
