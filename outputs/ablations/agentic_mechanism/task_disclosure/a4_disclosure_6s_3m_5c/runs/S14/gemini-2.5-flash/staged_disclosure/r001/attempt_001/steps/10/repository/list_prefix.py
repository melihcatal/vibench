import boto3

def list_objects_with_prefix(bucket_name, prefix):
    """
    Lists stored objects under a specific prefix in an S3 bucket.

    :param bucket_name: Name of the S3 bucket.
    :param prefix: The prefix to filter objects by.
    :return: A list of object keys matching the prefix.
    """
    s3 = boto3.client('s3')
    
    object_keys = []
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
    
    for page in pages:
        if "Contents" in page:
            for obj in page["Contents"]:
                object_keys.append(obj["Key"])
                
    return object_keys

if __name__ == "__main__":
    # Replace with your bucket name and desired prefix
    my_bucket_name = "your-s3-bucket-name" 
    my_prefix = "your-prefix/" 

    print(f"Listing objects in bucket '{my_bucket_name}' with prefix '{my_prefix}':")
    objects = list_objects_with_prefix(my_bucket_name, my_prefix)
    if objects:
        for key in objects:
            print(f"- {key}")
    else:
        print("No objects found with the specified prefix.")
