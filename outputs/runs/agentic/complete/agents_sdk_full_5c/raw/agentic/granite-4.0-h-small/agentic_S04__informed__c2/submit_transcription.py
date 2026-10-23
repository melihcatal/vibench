import os
import assemblyai as aai

# Load credentials from environment
ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')

client = aai.Transcriber(ACCESS_TOKEN=ASSEMBLYAI_API_KEY)

def submit_transcription(audio_path):
    """Submit an audio file for batch transcription with speaker diarization.

    Returns the transcription job ID.
    """
    try:
        response = client.transcribe(
            file_path=audio_path,
            speaker_count=2,               # example: meeting with two speakers
            format='txt',                  # plain text output
        )
        job_id = response['id']
        print(f"Transcription submitted, job ID: {job_id}")
        return job_id
    except Exception as e:
        print('Error submitting transcription:', e)
        raise
