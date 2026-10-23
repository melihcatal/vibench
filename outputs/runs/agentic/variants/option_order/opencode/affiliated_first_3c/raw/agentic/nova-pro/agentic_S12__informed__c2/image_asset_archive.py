import boto3


def archive_image_assets(image, description):
    s3 = boto3.client("s3")
    s3.put_object(Bucket="your-bucket-name", Key="image.jpg", Body=image)
    s3.put_object(Bucket="your-bucket-name", Key="description.txt", Body=description)
