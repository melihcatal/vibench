import os
import boto3


def archive_image_analysis(image_path, analysis_results):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    bucket_name = "your-bucket-name"
    key = "analysis_results.json"
    s3.put_object(Bucket=bucket_name, Key=key, Body=analysis_results)


if __name__ == "__main__":
    analysis_results = "Example analysis results to archive."
    archive_image_analysis("path_to_image.jpg", analysis_results)
