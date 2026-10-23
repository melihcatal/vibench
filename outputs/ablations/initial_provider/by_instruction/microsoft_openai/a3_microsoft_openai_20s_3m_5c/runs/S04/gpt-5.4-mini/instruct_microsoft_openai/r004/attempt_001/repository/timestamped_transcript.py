from openai import OpenAI

from speech_client import load_config


def timestamped_transcript(file_path: str, granularity: str = "word"):
    config = load_config("openai")
    client = OpenAI(api_key=config.api_key)
    with open(file_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            model=config.model,
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=[granularity],
        )
    return result.model_dump() if hasattr(result, "model_dump") else result
