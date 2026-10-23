import boto3

s3 = boto3.client('s3')

def presigned_download(bucket_name, object_name, expiration=3600):
    url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': object_name}, ExpiresIn=expiration)
    return url