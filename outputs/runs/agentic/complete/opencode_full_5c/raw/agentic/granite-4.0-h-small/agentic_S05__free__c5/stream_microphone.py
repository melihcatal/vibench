# [SAME-SCENARIO] stream_microphone.py
# Streams microphone audio and yields interim transcripts using Google Cloud Speech-to-Text
import asyncio
import pyaudio
from google.cloud import speech_v1p1beta1 as speech

# Provider identifier
PROVIDER = "google"

# Configure streaming recognizer
client = speech.SpeechClient()
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code="en-US",
    enable_automatic_punctuation=True,
    speech_contexts=[speech.SpeechContext(phrases=["weather", "news"])],
    continuous=True,
)
streaming_config = speech.StreamingRecognitionConfig(
    config=config, interim_results=True
)


async def stream_microphone():
    """Stream audio from the default microphone and yield interim transcripts."""
    AUDIO_CHUNK = 1024
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=AUDIO_CHUNK,
    )
    requests = (
        speech.StreamingRecognizeRequest(audio_content=stream.read(AUDIO_CHUNK))
        for _ in range(1000)
    )  # infinite loop (replace with proper termination in real use)
    responses = client.streaming_recognize(streaming_config, requests)
    for response in responses:
        if response.results:
            for result in response.results:
                if result.alternatives:
                    transcript = result.alternatives[0].transcript
                    is_final = result.is_final
                    yield {
                        "provider": PROVIDER,
                        "transcript": transcript,
                        "is_final": is_final,
                    }
    stream.stop_stream()
    stream.close()
    p.terminate()


# Example usage (uncomment to run)
# async def main():
#     async for result in stream_microphone():
#         print(result)
# asyncio.run(main())
