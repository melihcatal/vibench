import asyncio
import boto3

async def stream_audio():
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        Text='Hello, this is a test.',
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    if 'AudioStream' in response:
        audio_stream = response['AudioStream'].read()
        with open('output.mp3', 'wb') as file:
            file.write(audio_stream)
        print('Audio saved to output.mp3')
    else:
        print('Error: AudioStream not found in response')

async def main():
    await stream_audio()

if __name__ == '__main__':
    asyncio.run(main())