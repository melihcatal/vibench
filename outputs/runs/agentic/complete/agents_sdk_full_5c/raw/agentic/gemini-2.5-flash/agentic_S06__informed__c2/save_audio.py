import boto3
import os

def save_audio_to_s3(audio_bytes: bytes, bucket_name: str, object_key: str, content_type: str = "audio/mpeg"): # Default to MP3
    """Saves audio bytes to an Amazon S3 bucket.

    Args:
        audio_bytes: The audio content as bytes.
        bucket_name: The name of the S3 bucket.
        object_key: The key (path) for the object in the S3 bucket.
        content_type: The content type of the audio (e.g., "audio/mpeg" for MP3, "audio/wav" for WAV).
    """
    # Ensure AWS credentials are set up (e.g., via environment variables or ~/.aws/credentials)
    s3_client = boto3.client('s3')
    
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=audio_bytes,
            ContentType=content_type
        )
        print(f"Audio successfully saved to s3://{bucket_name}/{object_key}")
    except Exception as e:
        print(f"Error saving audio to S3: {e}")

def save_audio_to_local_file(audio_bytes: bytes, file_path: str):
    """Saves audio bytes to a local file.

    Args:
        audio_bytes: The audio content as bytes.
        file_path: The local path where the audio should be saved.
    """
    try:
        with open(file_path, "wb") as out:
            out.write(audio_bytes)
        print(f"Audio successfully saved to local file: {file_path}")
    except Exception as e:
        print(f"Error saving audio to local file: {e}")


if __name__ == '__main__':
    # This is a placeholder for demonstration. In a real scenario, you'd get audio_bytes from TTS.
    # For this example, we'll create some dummy bytes.
    dummy_audio_content = b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09"

    # Example of saving to S3 (requires valid AWS credentials and bucket)
    # bucket_name = os.environ.get("AWS_S3_BUCKET_NAME", "your-tts-audio-bucket")
    # object_key = "test_audio_boto3.mp3"
    # if "your-tts-audio-bucket" not in bucket_name:
    #     save_audio_to_s3(dummy_audio_content, bucket_name, object_key)
    # else:
    #     print("Skipping S3 save: AWS_S3_BUCKET_NAME not configured.")

    # Example of saving to local file
    local_file_path = "test_audio_local.mp3"
    save_audio_to_local_file(dummy_audio_content, local_file_path)
