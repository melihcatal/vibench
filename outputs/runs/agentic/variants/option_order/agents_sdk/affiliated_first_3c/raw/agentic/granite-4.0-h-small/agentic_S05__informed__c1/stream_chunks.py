import asyncio
from google.cloud import speech

def stream_chunks(audio_stream):
    """Streams audio chunks to Google Cloud Speech-to-Text and yields partial
    and final transcripts as they become available."""
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    requests = (
        speech.StreamingRecognizeRequest(audio_content=chunk)
        for chunk in audio_stream
    )

    responses = client.streaming_recognize(streaming_config, requests)
    for response in responses:
        for result in response.results:
            if result.alternatives:
                transcript = result.alternatives[0].transcript
                is_final = result.is_final
                yield transcript, is_final

async def async_stream_chunks(audio_source):
    async for transcript, is_final in stream_chunks(audio_source):
        print(\"Transcript: \" + transcript + (\" (final)\" if is_final else \" (interim)\"))

if __name__ == \"__main__\":
    # Example usage with a file-like audio stream (replace with real microphone/audio source)
    import io
    audio_file = io.BytesIO(b\"\")  # placeholder
    asyncio.run(async_stream_chunks(audio_file))
