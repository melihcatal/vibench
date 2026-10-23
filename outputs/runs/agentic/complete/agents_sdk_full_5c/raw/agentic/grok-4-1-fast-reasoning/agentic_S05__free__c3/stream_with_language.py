from speech_client import get_stt_client, get_live_options
from deepgram import LiveTranscriptionEvents

def start_streaming_recognizer(language='en', punctuation=True):
    client = get_stt_client()
    options = get_live_options(
        language=language,
        punctuate=punctuation
    )
    live = client.transcription.live(options)
    # Ready for handlers to be registered
    # e.g., live.registerHandler(LiveTranscriptionEvents.Transcript, handler)
    return live