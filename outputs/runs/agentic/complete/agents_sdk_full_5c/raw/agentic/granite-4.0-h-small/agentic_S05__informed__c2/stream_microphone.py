# [SAME-SCENARIO]
# Stream audio from the microphone using Amazon Transcribe Streaming
# Provider: Amazon Transcribe Streaming (AWS SDK boto3)
import asyncio
import boto3
import json
import pyaudio

# Configure AWS credentials via environment variables
# AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION

# Helper to read audio from microphone
DEBUG_MIC = False  # set True to pipe a test WAV file instead

STREAM_RATE = 16000
STREAM_WIDTH = 2
STREAM_CHANNELS = 1
FRAMES_PER_BUFFER = 1024

boto_client = boto3.client('transcribe')

def convert_to_signed_16(data):
    # data is bytes in default format (usually 16-bit signed)
    return data

async def main():
    # Start audio stream
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=STREAM_CHANNELS,
                    rate=STREAM_RATE,
                    input=True,
                    frames_per_buffer=FRAMES_PER_BUFFER)
    
    # Create a transcription stream
    transcription_stream = boto_client.start_stream_transcription(
        LanguageCode='en-US',
        MediaSampleRateHertz=STREAM_RATE,
        MediaEncoding='pcm',
    )
    # boto3 returns an iterable stream of results

    try:
        while True:
            audio = stream.read(FRAMES_PER_BUFFER)
            # Convert to signed 16-bit PCM if needed
            audio = convert_to_signed_16(audio)
            # Send audio to AWS (async supported via run_in_executor)
            # Here we use synchronous call; in production wrap with loop.run_in_executor
            boto_client.send_transcript(StreamARN=transcription_stream['StreamArn'], Data=audio)
            if DEBUG_MIC:
                # for demo, break after a few frames
                break
    except KeyboardInterrupt:
        print('Stopping stream.')
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        boto_client.stop_stream_transcription(StreamARN=transcription_stream['StreamArn'])

if __name__ == '__main__':
    asyncio.run(main())