from deepgram import LiveTranscriptionEvents

from speech_client import SpeechConfig, build_live_options, create_deepgram_client
from speech_models import TranscriptEvent, normalize_text


async def stream_with_language(language: str = "en-US"):
    cfg = SpeechConfig(
        api_key=create_deepgram_client().api_key, language=language, punctuate=True
    )
    client = create_deepgram_client(cfg)
    conn = await client.listen.asynclive.v("1")
    events = []

    def on_message(_, result, **__):
        alt = result.channel.alternatives[0]
        events.append(
            TranscriptEvent(
                text=normalize_text(alt.transcript),
                is_final=bool(result.channel.is_final),
                language=language,
                confidence=getattr(alt, "confidence", None),
            )
        )

    conn.on(LiveTranscriptionEvents.Transcript, on_message)
    await conn.start(build_live_options(cfg))
    return conn, events
