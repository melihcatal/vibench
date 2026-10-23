import pyaudio
import assemblyai as aai
from speech_client import get_transcriber

# Note: This requires PyAudio and a working microphone.
# You might need to install portaudio on your system.

def stream_from_microphone():
    """
    Streams audio from the microphone and yields transcripts from AssemblyAI.
    """
    transcriber = get_transcriber()

    def on_data(data: bytes):
        transcriber.stream(data)

    def on_error(error: Exception):
        print(f"An error occurred: {error}")

    def on_open():
        print("Streaming session started.")

    def on_close():
        print("Streaming session closed.")

    def on_transcript(transcript: aai.RealtimeTranscript):
        if not transcript.text:
            return

        if isinstance(transcript, aai.RealtimeFinalTranscript):
            yield transcript.text
        else:
            # Interim result
            yield transcript.text + "..."


    transcriber.connect(
        on_data=on_data,
        on_error=on_error,
        on_open=on_open,
        on_close=on_close,
    )

    # Open microphone stream
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1024,
        stream_callback=lambda in_data, frame_count, time_info, status: (
            on_data(in_data), (None, pyaudio.paContinue))
    )

    stream.start_stream()
    
    # The stream is non-blocking, so we need a way to keep the script running.
    # In a real application, this would be part of an event loop.
    # For this example, we will just wait for keyboard input to stop.
    try:
        input("Press Enter to stop streaming...\n")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        transcriber.close()
