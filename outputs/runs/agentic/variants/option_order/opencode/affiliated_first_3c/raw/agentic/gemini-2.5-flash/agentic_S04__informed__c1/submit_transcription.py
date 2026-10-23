import os
from speech_client import SpeechClient
from speech_models import TranscriptionJobRequest


def submit_transcription_job(request: TranscriptionJobRequest):
    client = SpeechClient().get_client()

    job_uri = request.media_uri

    settings = {"LanguageCode": request.language_code}

    if request.enable_speaker_diarization:
        settings["SpeakerDiarization"] = {
            "EnableSpeakerDiarization": True,
            "MaxSpeakerLabels": request.max_speakers,
        }
    if request.show_alternatives:
        settings["ShowAlternatives"] = True
        settings["MaxAlternatives"] = 2  # Defaulting to 2 alternatives

    if request.output_bucket_name:
        client.start_transcription_job(
            TranscriptionJobName=request.job_name,
            Media={"MediaFileUri": job_uri},
            OutputBucketName=request.output_bucket_name,
            **settings,
        )
    else:
        client.start_transcription_job(
            TranscriptionJobName=request.job_name,
            Media={"MediaFileUri": job_uri},
            **settings,
        )

    print(f"Transcription job {request.job_name} submitted successfully.")
