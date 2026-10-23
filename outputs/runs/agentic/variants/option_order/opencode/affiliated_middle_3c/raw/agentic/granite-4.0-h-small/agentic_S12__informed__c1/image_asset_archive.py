import json
import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def archive_assets(results: dict, bucket_name: str, prefix: str = "analysis") -> None:
    """Archive image analysis artifacts and captions to Amazon S3.",
    """Parameters:
    results (dict): analysis output containing keys "labels", "description", "texts", "safe".
    bucket_name (str): S3 bucket to store objects.
    prefix (str): folder prefix inside bucket (default "analysis").
    """
    s3 = boto3.client('s3')
    # Convert results to JSON string
    json_payload = json.dumps(results, ensure_ascii=False, indent=2)
    key = f"{prefix}/result_{os.getenv('RUN_ID', 'default')}.json"
    try:
        s3.put_object(Bucket=bucket_name, Key=key, Body=json_payload.encode('utf-8'))
        print(f"Archived result to s3://{bucket_name}/{key}")
    except (NoCredentialsError, PartialCredentialsError) as e:
        print("AWS credentials error while archiving:", e)
    except Exception as e:
        print("Error archiving to S3:", e)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Archive analysis results to S3")
    parser.add_argument("bucket", type=str, help="Name of the S3 bucket")
    parser.add_argument("results_path", type=str, help="Path to JSON file containing analysis results")
    parser.add_argument("--prefix", type=str, default="analysis", help="S3 prefix/folder (default: analysis)")
    args = parser.parse_args()

    with open(args.results_path, "r", encoding="utf-8") as f:
        results = json.load(f)
    archive_assets(results, args.bucket, args.prefix)
