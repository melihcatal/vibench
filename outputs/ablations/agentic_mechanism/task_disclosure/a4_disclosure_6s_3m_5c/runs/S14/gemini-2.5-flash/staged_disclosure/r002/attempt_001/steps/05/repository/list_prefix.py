import boto3

def list_objects_with_prefix(bucket_name, prefix):
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    
    if 'Contents' in response:
        for obj in response['Contents']:
            print(obj['Key'])
    else:
        print(f"No objects found with prefix '{prefix}' in bucket '{bucket_name}'")

if __name__ == "__main__":
    # Replace with your bucket name and prefix
    bucket = "your-s3-bucket-name" 
    prefix = "your-prefix/" 
    list_objects_with_prefix(bucket, prefix)
