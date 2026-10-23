# [SAME-SCENARIO] stream_chunks.py
# Streams audio chunks from an async source using Amazon Transcribe Streaming API
import asyncio
import boto3

# Amazon Transcribe authentication
AWS_ACCESS_KEY_ID = "${AWS_ACCESS_KEY_ID}"
AWS_SECRET_ACCESS_KEY = "${AWS_SECRET_ACCESS_KEY}"
REGION_NAME = "us-east-1"

# Audio configuration
AUDIO_FORMAT = "ogg-opus"
SAMPLE_RATE = 16000


async def stream_chunks(audio_source):
    transcriber = boto3.client(
        "transcribe",
        region_name=REGION_NAME,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    # Start a streaming transcription job
    job_name = "audio-stream-job"
    response = transcriber.start_stream_transcription(
        LanguageCode="en-US",
        MediaEncoding=AUDIO_FORMAT,
        SampleRate=str(SAMPLE_RATE),
        TranscriptFilter={
            "KeywordFilter": [{"Keywords": ["meeting", "project"]}]
        },  # Example filter
    )
    print(f"Started transcription job: {response['JobName']}")

    async for chunk in audio_source:
        # Send audio chunk to Transcribe
        transcriber.put_media_stream(
            StreamName=job_name,
            AudioChunk=chunk,
        )

    # Wait for completion (simplified)
    await asyncio.sleep(5)
    # Fetch final transcript (placeholder)
    result = transcriber.get_transcription_job(TranscriptionJobName=job_name)
    print(result)

    transcriber.stop_stream_transcription(StreamName=job_name)


if __name__ == "__main__":
    # Placeholder for audio source async generator
    stream_chunks(asyncio.sleep(10))
