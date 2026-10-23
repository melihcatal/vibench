import asyncio
import ibm_watson
import ibm_watson.streaming.base as asr_base

# Watson STT WebSocket credentials (environment variables)
API_KEY = os.getenv("IBM_STT_APIKEY")
URL = os.getenv("IBM_STT_URL")


async def stream_microphone():
    """Streams microphone audio to Watson Speech-to-Text WebSocket and yields interim transcripts."""
    config = ibm_watson.speech_to_text_v1.RecognizeStreamConfig(
        content_type="audio/l16; rate=16000",
        interim_results=True,
        continuous=True,
        model="en-US_BroadbandModel",
    )
    # Obtain a token via IAM
    token_manager = ibm_watson.IamAuthenticator(API_KEY)
    auth_token = token_manager.get_token()
    async for result in asr_base.recognize_stream(
        url=URL,
        config=config,
        auth_token=auth_token,
        audio_provider=asr_base.MicrophoneStream(),
    ):
        if result.alternatives and result.alternatives[0].transcript:
            yield result.alternatives[0].transcript


if __name__ == "__main__":
    # Simple demo: print each interim transcript
    transcriber = asyncio.run(stream_microphone())
    async for text in transcriber:
        print("Interim: ", text)
