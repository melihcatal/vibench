from speech_client import get_openai_client, get_transcription_model, open_audio
from speech_models import normalize_segments, normalize_words


def timestamped_transcript(audio_path, granularity="segment"):
    client = get_openai_client()
    with open_audio(audio_path) as audio:
        result = client.audio.transcriptions.create(
            model=get_transcription_model(),
            file=audio,
            response_format="verbose_json",
            timestamp_granularities=["word"] if granularity == "word" else ["segment"],
        )
    return {
        "words": normalize_words(getattr(result, "words", [])),
        "segments": normalize_segments(getattr(result, "segments", [])),
        "result": result,
    }
