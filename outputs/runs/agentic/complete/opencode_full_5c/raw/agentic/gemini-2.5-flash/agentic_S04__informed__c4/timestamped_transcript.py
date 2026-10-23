import os
import assemblyai as aai
from speech_client import get_assemblyai_client


def get_timestamped_transcript(audio_url: str) -> dict:
    """Returns word or segment timestamps from an AssemblyAI transcription result."""
    aai.settings.api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not aai.settings.api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    client = get_assemblyai_client()
    config = aai.TranscriptionConfig(
        audio_url=audio_url, word_boost=True
    )  # word_boost enables word-level timestamps
    transcript = client.transcribe(config.audio_url, config)

    if transcript.status == aai.TranscriptStatus.completed:
        word_timestamps = []
        for word in transcript.words:
            word_timestamps.append(
                {
                    "word": word.text,
                    "start": word.start,
                    "end": word.end,
                    "confidence": word.confidence,
                }
            )
        return {"words": word_timestamps}
    elif transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"Timestamped transcription failed: {transcript.error}")
    else:
        raise RuntimeError(
            f"Transcription job not completed yet. Current status: {transcript.status}"
        )


if __name__ == "__main__":
    # Example usage (replace with actual audio URL)
    # timestamped_result = get_timestamped_transcript("https://example.com/audio_with_timestamps.wav")
    # for word_info in timestamped_result["words"]:
    #     print(f"{word_info["word"]}: {word_info["start"]}-{word_info["end"]}")
    pass
