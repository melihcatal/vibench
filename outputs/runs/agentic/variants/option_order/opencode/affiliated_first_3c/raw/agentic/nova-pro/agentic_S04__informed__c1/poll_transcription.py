from speech_client import TRANSCRIBE_CLIENT


def poll_transcription(job_name):
    response = TRANSCRIBE_CLIENT.get_transcription_job(TranscriptionJobName=job_name)
    status = response["TranscriptionJob"]["TranscriptionJobStatus"]
    if status == "COMPLETED":
        transcript_uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
        with open("transcript.txt", "w") as f:
            f.write("Transcript fetched from: " + transcript_uri)
        return "Transcription completed"
    elif status == "FAILED":
        return "Transcription failed"
    else:
        return "Transcription in progress"
