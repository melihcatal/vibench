import os
import assemblyai as aai

class SpeechClient:
    """Helper wrapper for AssemblyAI batch speech-to-text APIs."""

    def __init__(self):
        # Load API key from env variable
        self.api_key = os.getenv('ASSEMBLYAI_API_KEY')
        if not self.api_key:
            raise RuntimeError('ASSEMBLYAI_API_KEY environment variable not set')
        self.client = aai.Transcriber(ACCESS_TOKEN=self.api_key)

    def submit(self, audio_path, speaker_count=2, include_diarization=False):
        """Submit a batch transcription job.
        Returns job ID.
        """
        try:
            response = self.client.transcribe(
                file_path=audio_path,
                format='json',
                speaker_count=speaker_count,
                diarization=include_diarization,
            )
            job_id = response.get('id')
            if not job_id:
                raise ValueError('Job ID not returned')
            print(f'Batch job submitted, ID: {job_id}')
            return job_id
        except Exception as e:
            print('Submission error:', e)
            raise

    def poll(self, job_id, poll_interval=5):
        """Poll a job until completion.
        Returns final transcript text.
        """
        while True:
            status_resp = self.client.get_transcription(job_id)
            status = status_resp.get('status')
            if status == 'completed':
                return status_resp.get('text')
            elif status in ('queued', 'processing'):
                print(f'Job {job_id} still {status}')
            else:
                err = status_resp.get('error', {}).get('message', 'unknown error')
                print('Job failed:', err)
                raise RuntimeError(err)
            time.sleep(poll_interval)

    def diarize(self, audio_path, speaker_count=2):
        """Submit a job with speaker diarization.
        Returns transcript text with speakers labeled.
        """
        return self.submit(audio_path, speaker_count, include_diarization=True)
