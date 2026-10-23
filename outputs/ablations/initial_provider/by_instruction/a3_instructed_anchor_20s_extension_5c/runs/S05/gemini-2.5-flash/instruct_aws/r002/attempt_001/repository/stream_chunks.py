
import asyncio
import os

from google.cloud import speech_v1p1beta1 as speech

# Google Cloud Speech-to-Text settings
GOOGLE_CLOUD_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
GOOGLE_CLOUD_SPEECH_LANGUAGE_CODE = os.environ.get("GOOGLE_CLOUD_SPEECH_LANGUAGE_CODE", "en-US")

async def stream_chunks_transcripts(audio_chunks_source):
    """
    Streams audio chunks from an async source to Google Cloud Speech-to-Text
    and yields interim transcripts.
    """
    client = speech.SpeechAsyncClient()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=GOOGLE_CLOUD_SPEECH_LANGUAGE_CODE,
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)

    # A generator that yields `StreamingRecognizeRequest` objects
    async def request_generator():
        yield speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        async for chunk in audio_chunks_source:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    try:
        responses = await client.streaming_recognize(requests=request_generator())

        async for response in responses:
            if not response.results:
                continue

            result = response.results[0]
            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript
            if result.is_final:
                yield transcript
            else:
                yield f"[Interim] {transcript}"

    except Exception as e:
        print(f"Error during Google Cloud Speech-to-Text streaming: {e}")
        yield f"[ERROR] {e}"
