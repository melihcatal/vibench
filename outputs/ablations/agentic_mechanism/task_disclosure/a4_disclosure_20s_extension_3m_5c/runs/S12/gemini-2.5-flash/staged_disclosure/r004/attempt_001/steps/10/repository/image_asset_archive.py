import boto3
import os

def archive_image_asset(bucket_name, artifact_filepath, caption_text, s3_client=None):
    """
    Archives an image-analysis artifact and its derived caption in AWS S3.

    Args:
        bucket_name (str): The name of the S3 bucket.
        artifact_filepath (str): The local path to the image artifact file.
        caption_text (str): The derived caption for the image.
        s3_client: Boto3 S3 client (optional). If not provided, a new one will be created.
    """
    if s3_client is None:
        s3_client = boto3.client('s3')

    # Upload the image artifact
    artifact_object_key = os.path.basename(artifact_filepath)
    print(f"Uploading artifact {artifact_filepath} to s3://{bucket_name}/{artifact_object_key}")
    s3_client.upload_file(artifact_filepath, bucket_name, artifact_object_key)
    print(f"Artifact {artifact_object_key} uploaded successfully.")

    # Upload the caption as a text file
    caption_object_key = f"{os.path.splitext(artifact_object_key)[0]}.txt"
    print(f"Uploading caption for {artifact_object_key} to s3://{bucket_name}/{caption_object_key}")
    s3_client.put_object(Bucket=bucket_name, Key=caption_object_key, Body=caption_text)
    print(f"Caption for {artifact_object_key} uploaded successfully.")

if __name__ == '__main__':
    # Example Usage:
    # Ensure you have AWS credentials configured (e.g., via environment variables or ~/.aws/credentials)
    # and replace 'your-s3-bucket-name' with your actual S3 bucket name.
    # Also, create a dummy image file for testing, e.g., 'test_image.jpg'

    # Create a dummy file for demonstration
    dummy_artifact_path = "test_image.jpg"
    with open(dummy_artifact_path, "w") as f:
        f.write("This is a dummy image artifact content.")

    s3_bucket = "your-s3-bucket-name"
    image_caption = "A beautiful sunset over the mountains."

    try:
        archive_image_asset(s3_bucket, dummy_artifact_path, image_caption)
        print("Archiving process completed.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up the dummy file
        if os.path.exists(dummy_artifact_path):
            os.remove(dummy_artifact_path)
            print(f"Cleaned up dummy artifact file: {dummy_artifact_path}")
