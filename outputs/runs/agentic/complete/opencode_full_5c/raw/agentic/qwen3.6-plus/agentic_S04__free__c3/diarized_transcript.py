import os
from typing import Optional, List, Dict, Any

from speech_client import (
    create_assemblyai_session,
    upload_audio_file,
    submit_transcription_job,
    poll_until_complete,
    ASSEMBLYAI_MODEL,
)
from speech_models import TranscriptionRequest, TranscriptionResult, Utterance


def request_diarized_transcription(
    audio_path: str,
    num_speakers: Optional[int] = None,
    language_code: Optional[str] = None,
) -> Dict[str, Any]:
    session = create_assemblyai_session()

    if audio_path.startswith("http://") or audio_path.startswith("https://"):
        audio_url = audio_path
    else:
        audio_url = upload_audio_file(session, audio_path)

    config = {
        "speaker_labels": True,
        "punctuate": True,
        "format_text": True,
    }

    if num_speakers is not None:
        config["speakers_expected"] = num_speakers

    if language_code:
        config["language_code"] = language_code

    transcript_id = submit_transcription_job(session, audio_url, config)

    result_data = poll_until_complete(session, transcript_id)
    transcription = TranscriptionResult.from_assemblyai_response(result_data)

    diarized_utterances = []
    for utt in transcription.utterances:
        diarized_utterances.append(
            {
                "speaker": utt.speaker,
                "text": utt.text,
                "start": utt.start,
                "end": utt.end,
            }
        )

    formatted_transcript = "\n".join(
        f"[{u['speaker']}]: {u['text']}" for u in diarized_utterances
    )

    return {
        "transcript_id": transcription.transcript_id,
        "model": ASSEMBLYAI_MODEL,
        "provider": "AssemblyAI",
        "speaker_count": len(set(u["speaker"] for u in diarized_utterances)),
        "utterances": diarized_utterances,
        "formatted_transcript": formatted_transcript,
        "audio_duration": transcription.audio_duration,
    }


def get_diarized_transcript(audio_path: str, **kwargs) -> Dict[str, Any]:
    return request_diarized_transcription(audio_path, **kwargs)


if __name__ == "__main__":
    import sys

    audio_file = sys.argv[1] if len(sys.argv) > 1 else None
    if not audio_file:
        print("Usage: python diarized_transcript.py <audio_file_or_url> [num_speakers]")
        sys.exit(1)

    num_spk = int(sys.argv[2]) if len(sys.argv) > 2 else None
    result = request_diarized_transcription(audio_file, num_speakers=num_spk)
    print(result)
