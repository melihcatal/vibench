from deepgram.types import LiveTranscriptResult, LiveAlternative
from speech_client import dg_client
from speech_models import get_live_options
from deepgram import LiveTranscriptionEvents, LiveOptions

def handle_partial_and_final():
    """Handles partial and final streaming recognition events from Deepgram."""
    partials = []
    finals = []
    def on_transcript(result: LiveTranscriptResult):
        if result.type == "Results" and result.channel and result.channel.alternatives:
            alt: LiveAlternative = result.channel.alternatives[0]
            transcript = alt.transcript
            if alt.is_final:
                finals.append(transcript)
            else:
                partials.append(transcript)

    options = get_live_options(interim_results=True)
    connection = dg_client.listen.live.v("1") \
        .registerCallback(LiveTranscriptionEvents.Transcript, on_transcript) \
        .start(options)
    return partials, finals, connection  # Example handling
