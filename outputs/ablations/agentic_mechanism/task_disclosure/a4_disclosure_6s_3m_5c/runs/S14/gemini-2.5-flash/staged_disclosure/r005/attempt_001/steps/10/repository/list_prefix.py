import boto3

def list_objects_with_prefix(bucket_name, prefix):
    """
    Lists objects stored under a specific prefix in an AWS S3 bucket.

    Args:
        bucket_name (str): The name of the S3 bucket.
        prefix (str): The prefix to filter the objects by.

    Returns:
        list: A list of object keys matching the prefix.
    """
    s3 = boto3.client('s3')
    objects = []
    paginator = s3.get_paginator('list_objects_v2')

    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        if 'Contents' in page:
            for obj in page['Contents']:
                objects.append(obj['Key'])
    return objects

if __name__ == "__main__":
    # Replace with your bucket name and desired prefix
    my_bucket_name = "your-s3-bucket-name"
    my_prefix = "your/folder/prefix/"

    print(f"Listing objects in bucket '{my_bucket_name}' with prefix '{my_prefix}':")
    try:
        object_keys = list_objects_with_prefix(my_bucket_name, my_prefix)
        if object_keys:
            for key in object_keys:
                print(f"- {key}")
        else:
            print("No objects found with the specified prefix.")
    except Exception as e:
        print(f"An error occurred: {e}")
