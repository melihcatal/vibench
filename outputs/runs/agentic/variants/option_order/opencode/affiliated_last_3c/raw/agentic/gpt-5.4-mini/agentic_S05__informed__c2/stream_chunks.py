from speech_client import build_deepgram_client, load_speech_config
from speech_models import normalize_event


async def stream_chunks(chunk_source):
    client = build_deepgram_client()
    cfg = load_speech_config()
    stream = client.transcription.live(
        {
            "language": cfg.language,
            "punctuate": cfg.punctuate,
            "interim_results": cfg.interim_results,
        }
    )
    async for chunk in chunk_source:
        await stream.send(chunk)
        event = await stream.recv()
        if event:
            yield normalize_event(
                {
                    "transcript": event.channel.alternatives[0].transcript
                    if event.channel.alternatives
                    else "",
                    "final": event.is_final,
                    "confidence": getattr(
                        event.channel.alternatives[0], "confidence", None
                    )
                    if event.channel.alternatives
                    else None,
                    "language": cfg.language,
                }
            )
