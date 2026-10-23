import boto3

S3_BUCKET = 'your-s3-bucket'

def archive_image(image_path, caption):
    s3 = boto3.client('s3')
    s3.upload_file(image_path, S3_BUCKET, image_path.split('/')[-1])
    metadata = {'caption': caption}
    s3.put_object_tagging(
        Bucket=S3_BUCKET,
        Key=image_path.split('/')[-1],
        Tagging={'TagSet': [{'Key': 'caption', 'Value': caption}]}
    )
    return 'Image and caption archived successfully.'