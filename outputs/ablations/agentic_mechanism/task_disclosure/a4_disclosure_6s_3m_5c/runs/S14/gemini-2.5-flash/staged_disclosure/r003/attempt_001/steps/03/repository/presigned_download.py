import boto3
from botocore.exceptions import ClientError

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
        print(e)
        return None

    # The response contains the presigned URL
    return response

if __name__ == '__main__':
    # Replace with your S3 bucket name and object key
    # For this example to work, you need to have AWS credentials configured
    # and an object named 'my-test-object.txt' in 'my-unique-bucket-name-12345'
    # in your S3 bucket.
    bucket_name = 'my-unique-bucket-name-12345'
    object_name = 'my-test-object.txt'
    
    presigned_url = create_presigned_url(bucket_name, object_name)
    if presigned_url:
        print(f"Presigned URL: {presigned_url}")
    else:
        print("Could not generate presigned URL.")
