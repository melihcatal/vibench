import sys

from speech_client import load_config, normalize_job_name


def diarized_transcript(audio_s3_uri: str, job_name: str = None):
    cfg = load_config()
    name = normalize_job_name(job_name or f"diarized-{audio_s3_uri.split('/')[-1]}")
    response = cfg.transcribe.start_transcription_job(
        TranscriptionJobName=name,
        Media={"MediaFileUri": audio_s3_uri},
        MediaFormat="mp3",
        LanguageCode=cfg.language_code,
        Settings={"ShowSpeakerLabels": True, "MaxSpeakerLabels": 10},
    )
    return response.get("TranscriptionJob", response)


if __name__ == "__main__":
    print(diarized_transcript(sys.argv[1]))
