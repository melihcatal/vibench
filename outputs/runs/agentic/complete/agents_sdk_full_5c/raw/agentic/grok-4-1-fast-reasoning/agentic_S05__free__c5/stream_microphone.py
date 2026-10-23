import pyaudio
import queue
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions
from deepgram.types import LiveTranscriptResult
from speech_client import dg_client
from speech_models import get_live_options

def stream_microphone():
    """Streams microphone audio and yields interim transcripts."""
    transcripts = []
    def on_transcript(result: LiveTranscriptResult):
        if result.type == "Results" and result.channel and result.channel.alternatives:
            transcripts.append(result.channel.alternatives[0].transcript)

    options = get_live_options()
    connection = dg_client.listen.live.v("1") \
        .registerCallback(LiveTranscriptionEvents.Transcript, on_transcript) \
        .start(options)

    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1024,
    )

    try:
        while True:
            data = stream.read(1024, exception_on_overflow=False)
            connection.send(data)
            while transcripts:
                yield transcripts.pop(0)
    except KeyboardInterrupt:
        pass
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        connection.finish()
