import pyaudio
import queue
import threading
from deepgram import LiveTranscriptionEvents
from speech_client import get_stt_client, get_live_options
from speech_models import extract_transcript

def stream_microphone():
    transcript_queue = queue.Queue()
    stop_event = threading.Event()

    def transcript_handler(transcript):
        text, is_final = extract_transcript(transcript)
        if text:
            transcript_queue.put((text, is_final))

    def close_handler(_):
        transcript_queue.put(None)

    client = get_stt_client()
    options = get_live_options()
    live = client.transcription.live(options)
    live.registerHandler(LiveTranscriptionEvents.Transcript, transcript_handler)
    live.registerHandler(LiveTranscriptionEvents.Close, close_handler)

    def microphone_sender():
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024
        )
        try:
            while not stop_event.is_set():
                data = stream.read(1024, exception_on_overflow=False)
                if live.socketOpened:
                    live.send(data)
        except Exception:
            pass
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
            live.finish()

    sender_thread = threading.Thread(target=microphone_sender, daemon=True)
    sender_thread.start()

    live.start()

    while True:
        item = transcript_queue.get()
        if item is None:
            break
        text, is_final = item
        yield text
        if is_final:
            yield f'[{text}]'  # Mark final

    sender_thread.join()