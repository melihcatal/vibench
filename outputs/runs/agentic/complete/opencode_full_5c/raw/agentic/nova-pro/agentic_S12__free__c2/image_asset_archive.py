import boto3


def archive_analysis(image_path, analysis_results):
    s3 = boto3.client("s3")
    s3.put_object(
        Bucket="my-image-analysis-bucket", Key=image_path, Body=analysis_results
    )
