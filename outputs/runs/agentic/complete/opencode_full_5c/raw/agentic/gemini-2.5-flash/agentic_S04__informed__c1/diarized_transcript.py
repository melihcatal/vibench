import os
from google.cloud import speech
from speech_client import get_speech_client
from speech_models import TranscriptionConfig, TranscriptionResult
from submit_transcription import submit_transcription_job
from poll_transcription import poll_transcription_job


def request_diarized_transcript(
    audio_uri: str, language_code: str = "en-US"
) -> TranscriptionResult:
    """Requests a transcription with speaker diarization for a recorded meeting.

    Args:
        audio_uri: URI of the audio file to transcribe.
        language_code: The language code of the audio.

    Returns:
        A TranscriptionResult object with diarization information.
    """
    config = TranscriptionConfig(
        audio_uri=audio_uri,
        language_code=language_code,
        enable_speaker_diarization=True,
        enable_word_time_offsets=True,  # Often needed for diarization to link words to speakers
    )

    print(f"Submitting diarization job for {audio_uri}...")
    operation_id = submit_transcription_job(config)
    print(f"Diarization job submitted with ID: {operation_id}. Polling for results...")

    result = poll_transcription_job(operation_id)

    # Process word_timestamps to extract speaker diarization for clarity
    if result.word_timestamps:
        diarization_speakers = []
        current_speaker_tag = None
        current_segment = {
            "speaker_tag": None,
            "start_time": None,
            "end_time": None,
            "words": [],
        }

        for word_info in result.word_timestamps:
            speaker_tag = word_info.get("speaker_tag")

            if speaker_tag is not None and speaker_tag != current_speaker_tag:
                # New speaker or first speaker
                if current_segment["words"]:
                    diarization_speakers.append(current_segment)
                current_speaker_tag = speaker_tag
                current_segment = {
                    "speaker_tag": speaker_tag,
                    "start_time": word_info["start_time"],
                    "end_time": word_info["end_time"],
                    "words": [word_info["word"]],
                }
            elif speaker_tag == current_speaker_tag:
                # Same speaker continues
                current_segment["words"].append(word_info["word"])
                current_segment["end_time"] = word_info["end_time"]
            else:
                # Handle cases where speaker_tag might be None or inconsistent, group as one speaker
                if current_segment["words"] and current_speaker_tag is None:
                    current_segment["words"].append(word_info["word"])
                    current_segment["end_time"] = word_info["end_time"]
                else:
                    if current_segment["words"]:
                        diarization_speakers.append(current_segment)
                    current_speaker_tag = None  # Reset for non-diarized segments
                    current_segment = {
                        "speaker_tag": None,
                        "start_time": word_info["start_time"],
                        "end_time": word_info["end_time"],
                        "words": [word_info["word"]],
                    }
        if current_segment["words"]:
            diarization_speakers.append(current_segment)

        result.diarization_speakers = diarization_speakers

    return result
