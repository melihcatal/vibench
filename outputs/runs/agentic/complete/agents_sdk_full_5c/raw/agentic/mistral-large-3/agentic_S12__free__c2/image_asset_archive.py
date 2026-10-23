import os
import boto3
from botocore.exceptions import NoCredentialsError
from typing import Dict, Any

def upload_to_s3(file_path: str, bucket_name: str, object_name: str) -> bool:
    """Uploads a file to an AWS S3 bucket."""
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        return True
    except NoCredentialsError:
        return False

def image_asset_archive(
    image_path: str,
    analysis_results: Dict[str, Any],
    bucket_name: str
) -> Dict[str, Any]:
    """Archives image and analysis artifacts in AWS S3."""
    image_object_name = f"images/{os.path.basename(image_path)}"
    results_object_name = f"results/{os.path.basename(image_path)}.json"
    
    image_success = upload_to_s3(image_path, bucket_name, image_object_name)
    results_success = upload_to_s3(
        analysis_results, bucket_name, results_object_name, is_json=True
    )
    
    return {
        "image_upload_success": image_success,
        "results_upload_success": results_success,
        "bucket": bucket_name,
        "image_object": image_object_name,
        "results_object": results_object_name
    }

def upload_to_s3(analysis_results: Dict[str, Any], bucket_name: str, object_name: str, is_json: bool = False) -> bool:
    """Helper to upload JSON results to S3."""
    import tempfile
    import json
    
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    
    try:
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as tmp_file:
            json.dump(analysis_results, tmp_file)
            tmp_file_path = tmp_file.name
        
        s3_client.upload_file(tmp_file_path, bucket_name, object_name)
        os.unlink(tmp_file_path)
        return True
    except (NoCredentialsError, Exception):
        return False