import queue
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions
from deepgram.types import LiveTranscriptResult
from speech_client import dg_client
from speech_models import get_live_options

def stream_chunks(audio_chunk_gen):
    """Streams audio chunks from a generator source and yields interim transcripts."""
    transcripts = []
    def on_transcript(result: LiveTranscriptResult):
        if result.type == "Results" and result.channel and result.channel.alternatives:
            transcripts.append(result.channel.alternatives[0].transcript)

    options = get_live_options()
    connection = dg_client.listen.live.v("1") \
        .registerCallback(LiveTranscriptionEvents.Transcript, on_transcript) \
        .start(options)

    try:
        for chunk in audio_chunk_gen:
            connection.send(chunk)
            while transcripts:
                yield transcripts.pop(0)
    finally:
        connection.finish()
