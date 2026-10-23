import time
from google.cloud import speech
from speech_client import get_speech_client, RATE

def generate_audio_chunks():
    """A generator that yields dummy audio chunks."""
    # In a real application, this could be reading from a file or network stream.
    num_chunks = 10
    for i in range(num_chunks):
        time.sleep(0.1)
        # Yield a dummy chunk of audio data
        yield b'\x00' * 3200

def stream_from_chunks():
    """Streams audio from a chunk generator to the Speech-to-Text API."""
    client = get_speech_client()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="en-US",
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True
    )

    def request_generator():
        for chunk in generate_audio_chunks():
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(streaming_config, request_generator())

    final_transcripts = []
    print("Processing audio chunks...")
    for response in responses:
        for result in response.results:
            if result.is_final:
                transcript = result.alternatives[0].transcript
                final_transcripts.append(transcript)
                print(f"Final transcript fragment: {transcript}")
            else:
                print(f"Interim transcript: {result.alternatives[0].transcript}")
                
    return final_transcripts
