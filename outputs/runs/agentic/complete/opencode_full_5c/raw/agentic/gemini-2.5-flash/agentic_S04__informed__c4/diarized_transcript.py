import os
import assemblyai as aai
from speech_client import get_assemblyai_client


def get_diarized_transcript(audio_url: str) -> dict:
    """Requests speaker diarization for a recorded meeting using AssemblyAI."""
    aai.settings.api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not aai.settings.api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    client = get_assemblyai_client()
    config = aai.TranscriptionConfig(audio_url=audio_url, diarization=True)
    transcript = client.transcribe(config.audio_url, config)

    if transcript.status == aai.TranscriptStatus.completed:
        # Access diarized segments
        diarized_segments = []
        for utterance in transcript.utterances:
            diarized_segments.append(
                {
                    "speaker": utterance.speaker,
                    "text": utterance.text,
                    "start": utterance.start,
                    "end": utterance.end,
                }
            )
        return {"segments": diarized_segments}
    elif transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"Diarization failed: {transcript.error}")
    else:
        raise RuntimeError(
            f"Diarization job not completed yet. Current status: {transcript.status}"
        )


if __name__ == "__main__":
    # Example usage (replace with actual audio URL)
    # diarized_result = get_diarized_transcript("https://example.com/meeting_audio.wav")
    # for segment in diarized_result["segments"]:
    #     print(f"Speaker {segment["speaker"]}: {segment["text"]} ({segment["start"]}-{segment["end"]})")
    pass
