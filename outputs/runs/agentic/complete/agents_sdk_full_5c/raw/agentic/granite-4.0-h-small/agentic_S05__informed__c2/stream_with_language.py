# [SAME-SCENARIO]
# Start a streaming transcription with language and punctuation settings using Amazon Transcribe Streaming
# Provider: Amazon Transcribe Streaming (AWS SDK boto3)
import boto3
import json

# Credentials are read from environment variables (AWS_ACCESS_KEY_ID, etc.)
boto_client = boto3.client('transcribe')

# Configure target language and enable punctuation (e.g., "en-US")
LANGUAGE_CODE = 'en-US'   # change as needed (e.g., 'es-ES' for Spanish)
ENABLE_PUNCTUATION = True  # Transcribe can insert punctuation where supported

async def start_stream(language_code=LANGUAGE_CODE, enable_punctuation=ENABLE_PUNCTUATION):
    # Start the streaming job and capture the StreamArn
    response = boto_client.start_stream_transcription(
        LanguageCode=language_code,
        EnablePunctuation=enable_punctuation,
        MediaSampleRateHertz=16000,
        MediaEncoding='pcm',
    )
    stream_arn = response['StreamArn']
    print(f'Started stream transcription (ARN: {stream_arn})')
    return stream_arn

if __name__ == '__main__':
    # For CLI demo, simply start the job and keep the ARN printed
    arn = boto_client.start_stream_transcription(
        LanguageCode=LANGUAGE_CODE,
        EnablePunctuation=ENABLE_PUNCTUATION,
        MediaSampleRateHertz=16000,
        MediaEncoding='pcm',
    )['StreamArn']
    print('Stream ARN:', arn)