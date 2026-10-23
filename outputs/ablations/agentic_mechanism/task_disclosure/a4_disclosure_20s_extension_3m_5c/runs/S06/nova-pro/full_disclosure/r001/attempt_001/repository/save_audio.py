import boto3

def save_audio(audio_stream, file_path):
    with open(file_path, 'wb') as file:
        file.write(audio_stream)

    print(f'Audio saved to {file_path}')

def save_audio_to_s3(audio_stream, bucket_name, object_key):
    s3_client = boto3.client('s3')
    s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=audio_stream)
    print(f'Audio saved to S3 bucket {bucket_name} with key {object_key}')

# Example usage:
# audio_stream = get_synthesized_audio()
# save_audio(audio_stream, 'output.mp3')
# save_audio_to_s3(audio_stream, 'my-audio-bucket', 'output.mp3')