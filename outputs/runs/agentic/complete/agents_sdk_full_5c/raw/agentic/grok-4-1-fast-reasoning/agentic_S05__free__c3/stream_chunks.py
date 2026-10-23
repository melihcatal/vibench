import queue
import threading
from deepgram import LiveTranscriptionEvents
from speech_client import get_stt_client, get_live_options
from speech_models import extract_transcript

def stream_chunks(audio_chunk_generator):
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

    def chunk_sender():
        try:
            for chunk in audio_chunk_generator:
                if live.socketOpened:
                    live.send(chunk)
        except Exception:
            pass
        finally:
            live.finish()

    sender_thread = threading.Thread(target=chunk_sender, daemon=True)
    sender_thread.start()

    live.start()

    while True:
        item = transcript_queue.get()
        if item is None:
            break
        text, is_final = item
        yield text