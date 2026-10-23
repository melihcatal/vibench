import os
from google.cloud import speech_v1 as speech

def poll_transcription_job(project_id, location, job_name):
    client = speech.SpeechClient()
    name = f"projects/{project_id}/locations/{location}/operations/{job_name}"

    while True:
        response = client.get_operation(name=name)
        if response.done:
            result = response.result()
            transcript = result.results[-1].alternatives[0].transcript
            return transcript
        else:
            print("Polling for transcription job...")
            time.sleep(10)

if __name__ == "__main__":
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    location = 'global'
    job_name = 'your-transcription-job-name'
    transcript = poll_transcription_job(project_id, location, job_name)
    print(f'Transcript: {transcript}')
