from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions
from speech_client import dg_client
from speech_models import get_live_options

def stream_with_language(language="fr-FR"):
    """Starts a streaming recognizer with language and punctuation settings."""
    options = get_live_options(
        model="nova-2",
        language=language,
        punctuate=True,
        interim_results=True
    )
    transcripts = []
    def on_transcript(result):
        if result.type == "Results" and result.channel and result.channel.alternatives:
            transcripts.append(result.channel.alternatives[0].transcript)

    connection = dg_client.listen.live.v("1") \
        .registerCallback(LiveTranscriptionEvents.Transcript, on_transcript) \
        .start(options)
    return connection, transcripts  # yields via list for demo
