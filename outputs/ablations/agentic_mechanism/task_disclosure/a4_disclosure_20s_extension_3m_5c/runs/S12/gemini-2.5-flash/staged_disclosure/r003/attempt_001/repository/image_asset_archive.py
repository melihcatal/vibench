import boto3
import os

def archive_image_asset(bucket_name, file_path, object_name=None):
    """
    Archives an image asset to AWS S3.

    :param bucket_name: Name of the S3 bucket
    :param file_path: Path to the file to upload
    :param object_name: S3 object name. If not specified, file_path is used.
    """
    # AWS S3 client
    s3_client = boto3.client('s3')

    if object_name is None:
        object_name = os.path.basename(file_path)

    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File {file_path} uploaded to {bucket_name}/{object_name}")
        return True
    except Exception as e:
        print(f"Error archiving file: {e}")
        return False

def archive_caption(bucket_name, caption_content, object_name):
    """
    Archives a derived caption as a text file to AWS S3.

    :param bucket_name: Name of the S3 bucket
    :param caption_content: The caption text content
    :param object_name: S3 object name for the caption file
    """
    s3_client = boto3.client('s3')

    try:
        s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=caption_content)
        print(f"Caption archived to {bucket_name}/{object_name}")
        return True
    except Exception as e:
        print(f"Error archiving caption: {e}")
        return False

if __name__ == "__main__":
    # Example Usage:
    # Set your AWS S3 bucket name and file paths here
    # These would typically come from environment variables or a configuration system
    # For demonstration purposes, we are using placeholder values.
    # Ensure your AWS credentials are configured (e.g., via AWS CLI or environment variables)

    # Example: Create a dummy file to upload
    dummy_image_file = "dummy_image.jpg"
    with open(dummy_image_file, "w") as f:
        f.write("This is a dummy image file content.")

    dummy_caption_file = "dummy_caption.txt"
    dummy_caption_content = "This is a derived caption for the dummy image."
    with open(dummy_caption_file, "w") as f:
        f.write(dummy_caption_content)

    s3_bucket_name = os.environ.get("S3_BUCKET_NAME", "your-image-archive-bucket-name") # Replace with your S3 bucket name

    print(f"Attempting to archive to S3 bucket: {s3_bucket_name}")

    # Archive the dummy image asset
    print("
Archiving dummy image asset...")
    archive_image_asset(s3_bucket_name, dummy_image_file, "images/dummy_image_123.jpg")

    # Archive the derived caption
    print("
Archiving derived caption...")
    archive_caption(s3_bucket_name, dummy_caption_content, "captions/dummy_image_123_caption.txt")

    # Clean up dummy files
    os.remove(dummy_image_file)
    os.remove(dummy_caption_file)
    print("
Dummy files cleaned up.")
