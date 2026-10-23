from deepgram import LiveTranscriptionEvents

from speech_client import normalize_transcript


def attach_partial_result_handlers(connection, on_partial=None, on_final=None):
    def handle_transcript(_, result, **__):
        alt = result.channel.alternatives[0]
        text = normalize_transcript(alt.transcript)
        if result.is_final:
            if on_final:
                on_final(text, result)
        elif on_partial:
            on_partial(text, result)

    connection.on(LiveTranscriptionEvents.Transcript, handle_transcript)
    return connection
