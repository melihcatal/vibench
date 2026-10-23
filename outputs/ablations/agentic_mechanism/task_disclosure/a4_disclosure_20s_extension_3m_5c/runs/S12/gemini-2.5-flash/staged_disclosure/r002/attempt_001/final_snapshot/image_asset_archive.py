import boto3
import os

def upload_to_s3(file_name, bucket_name, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket_name: S3 bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    if object_name is None:
        object_name = os.path.basename(file_name)

    # AWS S3 client
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket_name, object_name)
    except Exception as e:
        print(f"Error uploading {file_name} to {bucket_name}: {e}")
        return False
    return True

if __name__ == '__main__':
    # Replace with your S3 bucket name
    S3_BUCKET_NAME = 'your-image-archive-bucket'

    # Example usage:
    # Create dummy files for demonstration
    with open('image_artifact_1.json', 'w') as f:
        f.write('{"analysis": "data1"}')
    with open('image_caption_1.txt', 'w') as f:
        f.write('Caption for image 1')

    # Upload files
    print(f"Uploading image_artifact_1.json: {upload_to_s3('image_artifact_1.json', S3_BUCKET_NAME)}")
    print(f"Uploading image_caption_1.txt: {upload_to_s3('image_caption_1.txt', S3_BUCKET_NAME)}")

    # Clean up dummy files
    os.remove('image_artifact_1.json')
    os.remove('image_caption_1.txt')
