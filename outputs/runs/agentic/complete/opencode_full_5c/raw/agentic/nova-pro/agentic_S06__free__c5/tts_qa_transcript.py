import boto3


def transcribe_qa_transcript(audio_file):
    transcribe = boto3.client("transcribe")
    job_name = "qa-transcription-job"
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": audio_file},
        MediaFormat="mp3",
        LanguageCode="en-US",
    )
    # Wait for the job to complete and return the transcript
    # This is a simplified example; in practice, you would need to handle job status and results
    return "Transcription job started"
