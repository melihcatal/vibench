import boto3


def archive_image_assets(bucket_name, image_path, caption):
    s3_client = boto3.client("s3")
    s3_client.upload_file(
        image_path, bucket_name, "images/" + image_path.split("/")[-1]
    )
    s3_client.put_object(
        Bucket=bucket_name,
        Key="captions/" + image_path.split("/")[-1].replace(".jpg", ".txt"),
        Body=caption,
    )
