import os
import asyncio
import boto3
from botocore.exceptions import ClientError

from speech_client import get_aws_transcribe_client
from speech_models import TranscriptChunk

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")

async def start_transcribe_stream(
    audio_stream_generator,
    language_code: str,
    enable_punctuation: bool = True,
    sample_rate: int = 16000,
    encoding: str = "pcm"
):
    client = get_aws_transcribe_client(AWS_REGION)

    async def audio_generator():
        async for chunk in audio_stream_generator:
            yield {'AudioEvent': {'AudioChunk': chunk}}

    try:
        response = await client.start_stream_transcription(
            LanguageCode=language_code,
            MediaEncoding=encoding, # 'pcm' or 'ogg' or 'flac'
            SampleRateHertz=sample_rate,
            EnablePunctuation=enable_punctuation,
            VocabularyName=os.environ.get("AWS_TRANSCRIBE_VOCAB_NAME") if os.environ.get("AWS_TRANSCRIBE_VOCAB_NAME") else None,
            ContentIdentificationType='PII' if os.environ.get("AWS_TRANSCRIBE_PII_IDENTIFICATION") else None, # Example of more advanced feature
            AudioStream=audio_generator()
        )

        async for event in response['ResponseStream']:
            if 'TranscriptEvent' in event:
                transcript_event = event['TranscriptEvent']
                for result in transcript_event['Results']:
                    if result['Alternatives'] and result['Alternatives'][0]['Transcript']:
                        alternative = result['Alternatives'][0]
                        yield TranscriptChunk(
                            text=alternative['Transcript'],
                            start_time=result['StartTime'],
                            end_time=result['EndTime'],
                            is_final=result['IsPartial'] == False
                        )
    except ClientError as e:
        # Handle AWS Transcribe specific errors
        raise RuntimeError(f"AWS Transcribe error: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Error during transcription stream: {e}") from e
