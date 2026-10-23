import boto3

def stream_audio_chunks(bucket_name, object_key):
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    audio_stream = response['Body']
    chunk_size = 1024 * 1024  # 1 MB chunks
    while True:
        chunk = audio_stream.read(chunk_size)
        if not chunk:
            break
        yield chunk