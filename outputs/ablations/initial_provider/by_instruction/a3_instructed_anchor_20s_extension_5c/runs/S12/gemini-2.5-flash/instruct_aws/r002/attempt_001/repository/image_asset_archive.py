import boto3
import os

class ImageAssetArchiveRequest:
    def __init__(self, image_id: str, image_bytes: bytes, analysis_results: str, bucket_name: str):
        self.image_id = image_id
        self.image_bytes = image_bytes
        self.analysis_results = analysis_results
        self.bucket_name = bucket_name

class ImageAssetArchiveResponse:
    def __init__(self, image_url: str, results_url: str):
        self.image_url = image_url
        self.results_url = results_url

def image_asset_archive(request: ImageAssetArchiveRequest) -> ImageAssetArchiveResponse:
    s3_client = boto3.client('s3')

    # Upload original image
    image_key = f"images/{request.image_id}.jpg"
    s3_client.put_object(Bucket=request.bucket_name, Key=image_key, Body=request.image_bytes)
    image_url = f"https://{request.bucket_name}.s3.amazonaws.com/{image_key}"

    # Upload analysis results
    results_key = f"analysis-results/{request.image_id}.json"
    s3_client.put_object(Bucket=request.bucket_name, Key=results_key, Body=request.analysis_results.encode('utf-8'))
    results_url = f"https://{request.bucket_name}.s3.amazonaws.com/{results_key}"

    return ImageAssetArchiveResponse(image_url=image_url, results_url=results_url)
