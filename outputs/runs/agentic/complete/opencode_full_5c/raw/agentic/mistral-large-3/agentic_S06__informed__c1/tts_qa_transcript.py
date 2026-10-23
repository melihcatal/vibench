import boto3
import os


class TTSQATranscriber:
    def __init__(self):
        self.client = boto3.client(
            "transcribe",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def transcribe_audio(
        self, audio_file_uri: str, job_name: str = "transcription_job"
    ) -> str:
        self.client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={"MediaFileUri": audio_file_uri},
            MediaFormat="wav",
            LanguageCode="en-US",
        )

        while True:
            status = self.client.get_transcription_job(TranscriptionJobName=job_name)
            if status["TranscriptionJob"]["TranscriptionJobStatus"] in [
                "COMPLETED",
                "FAILED",
            ]:
                break

        if status["TranscriptionJob"]["TranscriptionJobStatus"] == "COMPLETED":
            transcript_uri = status["TranscriptionJob"]["Transcript"][
                "TranscriptFileUri"
            ]
            import requests

            response = requests.get(transcript_uri)
            return response.json()["results"]["transcripts"][0]["transcript"]
        else:
            raise Exception("Transcription job failed.")
