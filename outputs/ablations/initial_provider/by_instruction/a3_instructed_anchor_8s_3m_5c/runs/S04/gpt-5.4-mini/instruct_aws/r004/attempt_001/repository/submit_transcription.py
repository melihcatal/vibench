import os
import sys

from speech_client import load_config, normalize_job_name, s3_uri


def submit_transcription(audio_s3_uri: str, job_name: str = None, output_bucket: str = None):
    cfg = load_config()
    transcribe = cfg.transcribe
    name = normalize_job_name(job_name or os.path.basename(audio_s3_uri))
    kwargs = {
        "TranscriptionJobName": name,
        "Media": {"MediaFileUri": audio_s3_uri},
        "MediaFormat": "mp3",
        "LanguageCode": cfg.language_code,
        "OutputBucketName": output_bucket or cfg.bucket,
    }
    if cfg.vocabulary_name:
        kwargs["Settings"] = {"VocabularyName": cfg.vocabulary_name}
    response = transcribe.start_transcription_job(**{k: v for k, v in kwargs.items() if v})
    return response.get("TranscriptionJob", response)


if __name__ == "__main__":
    print(submit_transcription(sys.argv[1]))
