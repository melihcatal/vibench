from speech_client import TRANSCRIBE_CLIENT


def get_timestamps(job_name):
    response = TRANSCRIBE_CLIENT.get_transcription_job(TranscriptionJobName=job_name)
    if response["TranscriptionJob"]["TranscriptionJobStatus"] == "COMPLETED":
        transcript_uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
        with open("timestamps.txt", "w") as f:
            f.write("Timestamps fetched from: " + transcript_uri)
        return "Timestamps retrieved"
    else:
        return "Transcription not completed"
