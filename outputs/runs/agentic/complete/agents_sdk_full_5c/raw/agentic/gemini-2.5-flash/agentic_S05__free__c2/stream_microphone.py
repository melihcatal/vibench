import pyaudio
from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client, get_streaming_config
from speech_models import build_streaming_recognize_request

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms chunk

def listen_print_loop(responses):
    """Iterates through server responses and prints them."""
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        
        # Display interim results, overwrite previous line
        if not result.is_final:
            overwrite_chars = ' ' * (num_chars_printed - len(transcript))
            print(transcript + overwrite_chars + '\r', end='')
            num_chars_printed = len(transcript)
        else:
            print(transcript)
            num_chars_printed = 0
            yield transcript # Yield final transcripts

def stream_microphone_audio():
    """Streams audio from the microphone to Google Cloud Speech-to-Text."""
    client = get_speech_client()
    streaming_config = get_streaming_config()

    audio_interface = pyaudio.PyAudio()
    audio_stream = audio_interface.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    # A generator that yields audio chunks from the microphone
    def audio_generator():
        yield build_streaming_recognize_request(streaming_config=streaming_config) # Send config first
        while True:
            chunk = audio_stream.read(CHUNK, exception_on_overflow=False)
            if not chunk:
                break
            yield build_streaming_recognize_request(audio_content=chunk)

    requests = audio_generator()
    responses = client.streaming_recognize(requests)

    for transcript in listen_print_loop(responses):
        yield transcript
