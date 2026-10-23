import requests
from speech_client import SpeechClient
from speech_models import TranscriptionResult


def get_diarized_transcript(job_name: str) -> TranscriptionResult:
    client = SpeechClient().get_client()

    response = client.get_transcription_job(TranscriptionJobName=job_name)
    status = response["TranscriptionJob"]["TranscriptionJobStatus"]

    if status == "COMPLETED":
        transcript_file_uri = response["TranscriptionJob"]["Transcript"][
            "TranscriptFileUri"
        ]
        transcript_content = requests.get(transcript_file_uri).json()

        diarized_segments = []
        current_speaker = None
        current_text = ""

        for item in transcript_content["results"]["items"]:
            if "speaker_label" in item:
                speaker_label = item["speaker_label"]
                if speaker_label != current_speaker:
                    if current_speaker is not None:
                        diarized_segments.append(
                            {"speaker": current_speaker, "text": current_text.strip()}
                        )
                    current_speaker = speaker_label
                    current_text = item["alternatives"][0]["content"]
                else:
                    current_text += " " + item["alternatives"][0]["content"]
            else:  # Handle punctuation or non-speaker labeled items
                current_text += item["alternatives"][0]["content"]

        if current_speaker is not None:
            diarized_segments.append(
                {"speaker": current_speaker, "text": current_text.strip()}
            )

        return TranscriptionResult(
            job_name=job_name, status=status, diarized_segments=diarized_segments
        )
    else:
        return TranscriptionResult(
            job_name=job_name, status=status, diarized_segments=None
        )
